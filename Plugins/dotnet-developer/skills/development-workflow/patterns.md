# .NET Development Patterns

## Repository Pattern

```csharp
// Interface
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(T entity);
}

// Implementation
public class Repository<T> : IRepository<T> where T : class
{
    private readonly DbContext _context;
    private readonly DbSet<T> _dbSet;

    public Repository(DbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }

    public async Task<T?> GetByIdAsync(int id)
        => await _dbSet.FindAsync(id);

    public async Task<IEnumerable<T>> GetAllAsync()
        => await _dbSet.ToListAsync();

    public async Task AddAsync(T entity)
        => await _dbSet.AddAsync(entity);

    public async Task UpdateAsync(T entity)
        => _dbSet.Update(entity);

    public async Task DeleteAsync(T entity)
        => _dbSet.Remove(entity);
}
```

## Service Layer Pattern

```csharp
// Interface
public interface IOrderService
{
    Task<Order> CreateOrderAsync(CreateOrderRequest request);
    Task<Order?> GetOrderAsync(int id);
    Task CancelOrderAsync(int id);
}

// Implementation
public class OrderService : IOrderService
{
    private readonly IRepository<Order> _orderRepository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        IRepository<Order> orderRepository,
        IUnitOfWork unitOfWork,
        ILogger<OrderService> logger)
    {
        _orderRepository = orderRepository;
        _unitOfWork = unitOfWork;
        _logger = logger;
    }

    public async Task<Order> CreateOrderAsync(CreateOrderRequest request)
    {
        var order = new Order
        {
            CustomerId = request.CustomerId,
            Items = request.Items.Select(i => new OrderItem
            {
                ProductId = i.ProductId,
                Quantity = i.Quantity
            }).ToList(),
            Status = OrderStatus.Pending
        };

        await _orderRepository.AddAsync(order);
        await _unitOfWork.SaveChangesAsync();

        _logger.LogInformation("Order {OrderId} created", order.Id);
        return order;
    }
}
```

## Unit of Work Pattern

```csharp
public interface IUnitOfWork : IDisposable
{
    IRepository<Order> Orders { get; }
    IRepository<Customer> Customers { get; }
    Task<int> SaveChangesAsync();
}

public class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext _context;

    public UnitOfWork(AppDbContext context)
    {
        _context = context;
        Orders = new Repository<Order>(_context);
        Customers = new Repository<Customer>(_context);
    }

    public IRepository<Order> Orders { get; }
    public IRepository<Customer> Customers { get; }

    public async Task<int> SaveChangesAsync()
        => await _context.SaveChangesAsync();

    public void Dispose()
        => _context.Dispose();
}
```

## Result Pattern

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    private Result(bool isSuccess, T? value, string? error)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }

    public static Result<T> Success(T value)
        => new(true, value, null);

    public static Result<T> Failure(string error)
        => new(false, default, error);
}

// Usage
public async Task<Result<Order>> CreateOrderAsync(CreateOrderRequest request)
{
    if (request.Items.Count == 0)
        return Result<Order>.Failure("Order must have at least one item");

    var order = new Order { /* ... */ };
    await _repository.AddAsync(order);

    return Result<Order>.Success(order);
}
```

## Options Pattern

```csharp
// Configuration class
public class EmailSettings
{
    public const string SectionName = "Email";

    public string SmtpHost { get; set; } = string.Empty;
    public int SmtpPort { get; set; }
    public string FromAddress { get; set; } = string.Empty;
}

// Registration
services.Configure<EmailSettings>(
    configuration.GetSection(EmailSettings.SectionName));

// Usage
public class EmailService
{
    private readonly EmailSettings _settings;

    public EmailService(IOptions<EmailSettings> options)
    {
        _settings = options.Value;
    }
}
```

## Factory Pattern

```csharp
public interface INotificationFactory
{
    INotification Create(NotificationType type);
}

public class NotificationFactory : INotificationFactory
{
    private readonly IServiceProvider _serviceProvider;

    public NotificationFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public INotification Create(NotificationType type) => type switch
    {
        NotificationType.Email => _serviceProvider.GetRequiredService<EmailNotification>(),
        NotificationType.Sms => _serviceProvider.GetRequiredService<SmsNotification>(),
        NotificationType.Push => _serviceProvider.GetRequiredService<PushNotification>(),
        _ => throw new ArgumentOutOfRangeException(nameof(type))
    };
}
```

## Specification Pattern

```csharp
public interface ISpecification<T>
{
    Expression<Func<T, bool>> Criteria { get; }
    List<Expression<Func<T, object>>> Includes { get; }
}

public abstract class Specification<T> : ISpecification<T>
{
    public abstract Expression<Func<T, bool>> Criteria { get; }
    public List<Expression<Func<T, object>>> Includes { get; } = new();

    protected void AddInclude(Expression<Func<T, object>> include)
        => Includes.Add(include);
}

// Usage
public class ActiveOrdersSpec : Specification<Order>
{
    public override Expression<Func<Order, bool>> Criteria
        => o => o.Status != OrderStatus.Cancelled && o.Status != OrderStatus.Completed;

    public ActiveOrdersSpec()
    {
        AddInclude(o => o.Customer);
        AddInclude(o => o.Items);
    }
}
```

## Mediator Pattern (MediatR)

```csharp
// Query
public record GetOrderQuery(int Id) : IRequest<Order?>;

public class GetOrderHandler : IRequestHandler<GetOrderQuery, Order?>
{
    private readonly IRepository<Order> _repository;

    public GetOrderHandler(IRepository<Order> repository)
    {
        _repository = repository;
    }

    public async Task<Order?> Handle(GetOrderQuery request, CancellationToken ct)
    {
        return await _repository.GetByIdAsync(request.Id);
    }
}

// Command
public record CreateOrderCommand(int CustomerId, List<OrderItemDto> Items) : IRequest<Order>;

public class CreateOrderHandler : IRequestHandler<CreateOrderCommand, Order>
{
    public async Task<Order> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        // Implementation
    }
}
```

## Guard Clauses

```csharp
public static class Guard
{
    public static void AgainstNull<T>(T? value, string paramName) where T : class
    {
        if (value is null)
            throw new ArgumentNullException(paramName);
    }

    public static void AgainstEmpty(string? value, string paramName)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Value cannot be empty", paramName);
    }

    public static void AgainstNegative(int value, string paramName)
    {
        if (value < 0)
            throw new ArgumentOutOfRangeException(paramName, "Value cannot be negative");
    }
}

// Usage
public void Process(Order order, int quantity)
{
    Guard.AgainstNull(order, nameof(order));
    Guard.AgainstNegative(quantity, nameof(quantity));

    // Main logic
}
```

## Decorator Pattern

```csharp
// Interface
public interface INotificationService
{
    Task SendAsync(Notification notification);
}

// Base implementation
public class EmailNotificationService : INotificationService
{
    public async Task SendAsync(Notification notification)
    {
        // Send email
    }
}

// Decorator
public class LoggingNotificationDecorator : INotificationService
{
    private readonly INotificationService _inner;
    private readonly ILogger<LoggingNotificationDecorator> _logger;

    public LoggingNotificationDecorator(
        INotificationService inner,
        ILogger<LoggingNotificationDecorator> logger)
    {
        _inner = inner;
        _logger = logger;
    }

    public async Task SendAsync(Notification notification)
    {
        _logger.LogInformation("Sending notification to {Recipient}", notification.Recipient);
        await _inner.SendAsync(notification);
        _logger.LogInformation("Notification sent successfully");
    }
}

// Registration
services.AddScoped<EmailNotificationService>();
services.AddScoped<INotificationService>(sp =>
    new LoggingNotificationDecorator(
        sp.GetRequiredService<EmailNotificationService>(),
        sp.GetRequiredService<ILogger<LoggingNotificationDecorator>>()));
```
