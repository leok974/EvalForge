# Cloud Logging Alert Setup for Vertex AI Errors

## Quick Setup (CLI)

### Alert for 404 NOT_FOUND errors
```bash
gcloud logging metrics create vertex_404_errors \
  --description="Vertex AI 404 NOT_FOUND errors" \
  --log-filter='resource.type="cloud_run_revision"
    AND resource.labels.service_name="evalforge-agents"
    AND textPayload:"404 NOT_FOUND"
    AND textPayload:"aiplatform.googleapis.com"'

gcloud alpha monitoring policies create \
  --notification-channels=YOUR_CHANNEL_ID \
  --display-name="Vertex AI 404 Errors" \
  --condition-display-name="404 errors detected" \
  --condition-threshold-value=1 \
  --condition-threshold-duration=60s \
  --condition-filter='metric.type="logging.googleapis.com/user/vertex_404_errors"
    AND resource.type="cloud_run_revision"'
```

### Alert for 403 PERMISSION_DENIED errors
```bash
gcloud logging metrics create vertex_403_errors \
  --description="Vertex AI 403 PERMISSION_DENIED errors" \
  --log-filter='resource.type="cloud_run_revision"
    AND resource.labels.service_name="evalforge-agents"
    AND textPayload:"403 PERMISSION_DENIED"
    AND textPayload:"aiplatform.googleapis.com"'

gcloud alpha monitoring policies create \
  --notification-channels=YOUR_CHANNEL_ID \
  --display-name="Vertex AI 403 Errors" \
  --condition-display-name="Permission denied errors detected" \
  --condition-threshold-value=1 \
  --condition-threshold-duration=60s \
  --condition-filter='metric.type="logging.googleapis.com/user/vertex_403_errors"
    AND resource.type="cloud_run_revision"'
```

## Manual Setup (Console)

### Step 1: Create Log-Based Metrics

1. Go to **Logging** → **Logs-based Metrics**
2. Click **CREATE METRIC**
3. For 404 errors:
   - Name: `vertex_404_errors`
   - Filter:
     ```
     resource.type="cloud_run_revision"
     resource.labels.service_name="evalforge-agents"
     textPayload:"404 NOT_FOUND"
     textPayload:"aiplatform.googleapis.com"
     ```
   - Type: Counter
4. Repeat for 403 errors with filter:
   ```
   resource.type="cloud_run_revision"
   resource.labels.service_name="evalforge-agents"
   textPayload:"403 PERMISSION_DENIED"
   textPayload:"aiplatform.googleapis.com"
   ```

### Step 2: Create Alert Policies

1. Go to **Monitoring** → **Alerting**
2. Click **CREATE POLICY**
3. Add condition:
   - Resource type: **Cloud Run Revision**
   - Metric: **User-defined metrics** → Select your log metric
   - Threshold: **Above** 1 for 1 minute
4. Configure notifications:
   - Add notification channel (email, Slack, PagerDuty, etc.)
5. Set documentation:
   ```
   Vertex AI error detected in EvalForge service.
   
   Troubleshooting steps:
   1. Check Cloud Run environment variables
   2. Verify model name and region match
   3. Confirm IAM roles are correct
   4. Check Model Garden availability
   ```

## Test the Alerts

```bash
# View recent logs to confirm filter works
gcloud logging read 'resource.type="cloud_run_revision"
  AND resource.labels.service_name="evalforge-agents"
  AND (textPayload:"404 NOT_FOUND" OR textPayload:"403 PERMISSION_DENIED")
  AND textPayload:"aiplatform.googleapis.com"' \
  --limit=10 \
  --format='value(timestamp,textPayload)'
```

## Notification Channels

### Create Email Notification
```bash
gcloud alpha monitoring channels create \
  --display-name="EvalForge Alerts Email" \
  --type=email \
  --channel-labels=email_address=YOUR_EMAIL@example.com
```

### Create Slack Notification
```bash
gcloud alpha monitoring channels create \
  --display-name="EvalForge Alerts Slack" \
  --type=slack \
  --channel-labels=url=YOUR_SLACK_WEBHOOK_URL
```

### List Existing Channels
```bash
gcloud alpha monitoring channels list
```

## Common Log Filters

### All Vertex AI Errors
```
resource.type="cloud_run_revision"
resource.labels.service_name="evalforge-agents"
(textPayload:"NOT_FOUND" OR textPayload:"PERMISSION_DENIED" OR textPayload:"INVALID_ARGUMENT")
textPayload:"aiplatform.googleapis.com"
```

### Model-Specific Errors
```
resource.type="cloud_run_revision"
resource.labels.service_name="evalforge-agents"
textPayload:"Publisher Model"
textPayload:"not found"
```

### ADC/Authentication Errors
```
resource.type="cloud_run_revision"
resource.labels.service_name="evalforge-agents"
(textPayload:"default credentials" OR textPayload:"authentication")
severity>=ERROR
```

## Alert Thresholds

**Recommended settings:**
- **404 errors**: Alert immediately (threshold=1, duration=1min)
- **403 errors**: Alert immediately (threshold=1, duration=1min)
- **General errors**: Alert after 3 occurrences in 5 minutes

## Dashboard Query

Create a dashboard to monitor:
```
fetch cloud_run_revision
| metric 'logging.googleapis.com/user/vertex_404_errors'
| group_by 1m, [value_vertex_404_errors_mean: mean(value.vertex_404_errors)]
```
