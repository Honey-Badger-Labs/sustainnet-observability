# Family Meal Planner API - Prometheus Instrumentation Guide

This guide shows how to add Prometheus metrics to the FMP Node.js API for observability.

## Installation

Install the Prometheus client library:

```bash
npm install prom-client
```

## Basic Setup

Create `src/metrics/prometheus.js`:

```javascript
const client = require('prom-client');

// Create a Registry to register metrics
const register = new client.Registry();

// Add default metrics (CPU, memory, event loop, etc.)
client.collectDefaultMetrics({ register });

// Custom Metrics

// HTTP Request Duration Histogram
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.001, 0.01, 0.05, 0.1, 0.5, 1, 2, 5]
});
register.registerMetric(httpRequestDuration);

// HTTP Request Total Counter
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
});
register.registerMetric(httpRequestsTotal);

// Database Query Duration Histogram
const databaseQueryDuration = new client.Histogram({
  name: 'database_query_duration_seconds',
  help: 'Duration of database queries in seconds',
  labelNames: ['operation', 'model'],
  buckets: [0.001, 0.01, 0.05, 0.1, 0.5, 1, 2]
});
register.registerMetric(databaseQueryDuration);

// Database Connection Gauge
const databaseConnections = new client.Gauge({
  name: 'database_connections_active',
  help: 'Number of active database connections'
});
register.registerMetric(databaseConnections);

// Authentication Metrics
const authLoginAttempts = new client.Counter({
  name: 'auth_login_attempts_total',
  help: 'Total number of login attempts',
  labelNames: ['status']
});
register.registerMetric(authLoginAttempts);

const authLoginSuccess = new client.Counter({
  name: 'auth_login_success_total',
  help: 'Total number of successful logins',
  labelNames: ['user_id']
});
register.registerMetric(authLoginSuccess);

const authLoginFailures = new client.Counter({
  name: 'auth_login_failures_total',
  help: 'Total number of failed login attempts',
  labelNames: ['reason']
});
register.registerMetric(authLoginFailures);

// Business Metrics
const recipeSearches = new client.Counter({
  name: 'recipe_searches_total',
  help: 'Total number of recipe searches',
  labelNames: ['user_id']
});
register.registerMetric(recipeSearches);

const mealPlansCreated = new client.Counter({
  name: 'meal_plans_created_total',
  help: 'Total number of meal plans created',
  labelNames: ['family_id']
});
register.registerMetric(mealPlansCreated);

const familyInvitationsSent = new client.Counter({
  name: 'family_invitations_sent_total',
  help: 'Total number of family invitations sent'
});
register.registerMetric(familyInvitationsSent);

const familyInvitationsAccepted = new client.Counter({
  name: 'family_invitations_accepted_total',
  help: 'Total number of family invitations accepted'
});
register.registerMetric(familyInvitationsAccepted);

// Redis Metrics
const redisHits = new client.Counter({
  name: 'redis_hits_total',
  help: 'Total number of Redis cache hits'
});
register.registerMetric(redisHits);

const redisMisses = new client.Counter({
  name: 'redis_misses_total',
  help: 'Total number of Redis cache misses'
});
register.registerMetric(redisMisses);

module.exports = {
  register,
  httpRequestDuration,
  httpRequestsTotal,
  databaseQueryDuration,
  databaseConnections,
  authLoginAttempts,
  authLoginSuccess,
  authLoginFailures,
  recipeSearches,
  mealPlansCreated,
  familyInvitationsSent,
  familyInvitationsAccepted,
  redisHits,
  redisMisses
};
```

## Middleware Setup

Create `src/middleware/metricsMiddleware.js`:

```javascript
const { httpRequestDuration, httpRequestsTotal } = require('../metrics/prometheus');

function metricsMiddleware(req, res, next) {
  const start = Date.now();
  
  // Record request
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000; // Convert to seconds
    const route = req.route ? req.route.path : req.path;
    const labels = {
      method: req.method,
      route: route,
      status_code: res.statusCode,
      status: res.statusCode < 400 ? '2xx-3xx' : res.statusCode < 500 ? '4xx' : '5xx'
    };
    
    httpRequestDuration.observe(labels, duration);
    httpRequestsTotal.inc(labels);
  });
  
  next();
}

module.exports = metricsMiddleware;
```

## Add Metrics Endpoint

In `src/server.js` or `src/app.js`:

```javascript
const express = require('express');
const { register } = require('./metrics/prometheus');
const metricsMiddleware = require('./middleware/metricsMiddleware');

const app = express();

// Add metrics middleware to all routes
app.use(metricsMiddleware);

// Metrics endpoint (should be protected in production)
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

// ... rest of your app
```

## Instrument Authentication

In your auth controller (`src/controllers/authController.js`):

```javascript
const { authLoginAttempts, authLoginSuccess, authLoginFailures } = require('../metrics/prometheus');

async function login(req, res) {
  const { email, password } = req.body;
  
  authLoginAttempts.inc({ status: 'attempted' });
  
  try {
    const user = await User.findOne({ where: { email } });
    
    if (!user) {
      authLoginFailures.inc({ reason: 'user_not_found' });
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const isValidPassword = await bcrypt.compare(password, user.password);
    
    if (!isValidPassword) {
      authLoginFailures.inc({ reason: 'invalid_password' });
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    authLoginSuccess.inc({ user_id: user.id });
    
    // ... generate token, return response
  } catch (error) {
    authLoginFailures.inc({ reason: 'server_error' });
    throw error;
  }
}
```

## Instrument Database Queries

Wrap Sequelize queries with timing:

```javascript
const { databaseQueryDuration, databaseConnections } = require('../metrics/prometheus');

// Hook into Sequelize
sequelize.addHook('beforeQuery', (options) => {
  options.startTime = Date.now();
});

sequelize.addHook('afterQuery', (options) => {
  const duration = (Date.now() - options.startTime) / 1000;
  const model = options.model ? options.model.name : 'unknown';
  const operation = options.type; // SELECT, INSERT, UPDATE, DELETE
  
  databaseQueryDuration.observe({ operation, model }, duration);
});

// Update connection count periodically
setInterval(() => {
  const pool = sequelize.connectionManager.pool;
  databaseConnections.set(pool.size - pool.available);
}, 5000);
```

## Instrument Business Metrics

In your controllers:

```javascript
const { recipeSearches, mealPlansCreated, familyInvitationsSent } = require('../metrics/prometheus');

// Recipe search
async function searchRecipes(req, res) {
  recipeSearches.inc({ user_id: req.user.id });
  
  // ... search logic
}

// Meal plan creation
async function createMealPlan(req, res) {
  const mealPlan = await MealPlan.create({ ...req.body });
  mealPlansCreated.inc({ family_id: req.user.familyId });
  
  // ... response
}

// Family invitation
async function sendInvitation(req, res) {
  familyInvitationsSent.inc();
  
  // ... send email logic
}
```

## Instrument Redis Cache

Wrap your Redis client:

```javascript
const { redisHits, redisMisses } = require('../metrics/prometheus');

const originalGet = redisClient.get.bind(redisClient);
redisClient.get = async function(key) {
  const value = await originalGet(key);
  
  if (value !== null) {
    redisHits.inc();
  } else {
    redisMisses.inc();
  }
  
  return value;
};
```

## Testing Metrics

Start your API and visit:
```
http://localhost:3001/metrics
```

You should see Prometheus-formatted metrics like:

```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="POST",route="/api/auth/login",status="2xx-3xx"} 42

# HELP http_request_duration_seconds Duration of HTTP requests in seconds
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{method="GET",route="/api/recipes",status_code="200",le="0.1"} 150
```

## Next Steps

1. Add these metrics to your FMP API
2. Run `setup-local-demo.sh` to start Prometheus + Grafana
3. View dashboards at http://localhost:3000
4. Verify metrics are being collected

## Production Considerations

- **Protect `/metrics` endpoint**: Add authentication in production
- **High cardinality labels**: Avoid user IDs in labels (use aggregation instead)
- **Performance**: Metrics collection has minimal overhead (~1-2ms per request)
- **Retention**: Configure Prometheus retention period (default 15 days)
