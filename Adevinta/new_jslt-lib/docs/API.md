
# API

Overall description of functions defined in the API. Tests don't lie, so check for specific and detailed behaviour 
in the tests.

## `lib/commons.jslt`

| Function | Description |
| :------- | :---------- |
| `canned-client-id` | Captures _client_ from SDRN provider |

## `lib/schemas.jslt`

| Function | Description |
| :------- | :---------- |
| `deploy-stage-values()` | Deploy Stage values defined in `deployStage` in [event-formats base-routable-event.json](https://github.mpi-internal.com/spt-dataanalytics/event-formats/blob/master/schema/master/events/base-routable-event.json). |
| `device-type-values()` | Device Types values defined in `deviceType` in [event-formats Device.json](https://github.mpi-internal.com/spt-dataanalytics/event-formats/blob/master/schema/master/objects/Device.json). |
| `event-name-values()` | List of event names returned by `get-event-name()`. |
| `event-type-values()` | Event Types values defined in `eventTypes` in [event-formats common-definitions.json](https://github.mpi-internal.com/spt-dataanalytics/event-formats/blob/master/schema/master/common-definitions.json). |
| `get-event-name(event)` | Returns a name for the event, based on the underlying event type, the object type and, the object's `inReplyTo` type. See [Backend Events](https://data.mpi-internal.com/200-governance/100-schema-governance/100-events-catalog/200-backend-events/), [Frontend Events](https://data.mpi-internal.com/200-governance/100-schema-governance/100-events-catalog/100-frontend-events/) |
| `get-event-type(event)` | Returns the event's `.@type`. Includes fallback for alternate spelling of field names. |
| `get-object-in-reply-to-type(event)` | Returns the event's `.object.inReplyTo.@type`. Includes fallback for alternate spelling of field names. |
| `get-object-type(event)` | Returns the event's `.object.@type`. Includes fallback for alternate spelling of field names. |
| `get-tracker-type(event)` | Returns the event's `.tracker.@type`. Includes fallback for alternate spelling of field names. |
| `object-type-values()` | Object Types values defined in `content` in [event-formats common-definitions.json](https://github.mpi-internal.com/spt-dataanalytics/event-formats/blob/master/schema/master/common-definitions.json). |
| `provider-ids()` | MPI Provider (aka Data Owner) identifiers. |
| `provider-product-type-values()` | Provider product type values defined in `productType` in [event-formats Provider.json](https://github.mpi-internal.com/spt-dataanalytics/event-formats/blob/master/schema/master/objects/Provider.json). |
| `tracker-type-values()` | Tracker Types values defined in `type` in [event-formats Tracker.json](https://github.mpi-internal.com/spt-dataanalytics/event-formats/blob/master/schema/master/objects/Tracker.json). |

## `lib/metrics.jslt`

Base functionality for the composition of metrics.

| Function | Description |
| :------- | :---------- |
| `metric(suffix, delta)` | Generates a counter metric with the given `suffix` and `delta` as the increment value |
| `tagged-metric(suffix, delta, tag-key, tag-value)` | Generates a counter metric with the given `suffix`, `delta` as the increment value and additionally tagged with the given `tag-key` and `tag-value` pair |
| `taggify(tag-value, fallback-value, whitelisted-values)` | Helper function to safely generate tagged values. It checks that the given `tag-value` is not `null` string, otherwise `fallback-value` is returned. `whitelisted-values` must be a non-null array and it checks that the given `tag-value` is in the whitelisted list, otherwise `fallback-value` is returned. |

!!! danger "Be aware of the costs of the metrics"
    Cost of metrics is determined by the number of unique combinations of metrics and tags, so 
    uncontrolled tags may result on unexpected costs. Using whitelisted values is a way to keep costs 
    under control.

## `checks/commons.jslt`

### `check`

Special mention to `check` function, which is the base for 
[_Data Quality Checks_](data-quality-checks.md). 

```
def check(check-suite, check-name, check-result, tag-object, check-impact)
```

It has following arguments:

- `check-suite`: _Check Suite_ name
- `check-name`: _Check_ name
- `check-result`: Check result. It must be a binary/logical expression. The check passes or not.
- `tag-object`: User tags. Dictionary with the user tags (to be built by using `tag` and `taggify` methods in `lib/metrics`). Number of user tags is restricted to max 5.
- `check-impact`: Allowed values are: `blocker`, `critical`, `minor`. If given value is not one
  of the allowed ones, `critical` will be used instead.

As with `metric`, composition is allowed for `check` with `+`
Example:

```
import "lib/metrics.jslt" as m
import "lib/schemas.jslt" as s
import "checks/commons.jslt" as c

let trackerTypeTag = m:tag("tracker", m:taggify(s:get-tracker-type(.), "unknown",  s:tracker-type-values()))
let objectTypeTag = m:tag("object-type", m:taggify(s:get-object-type(.), "unknown", s:object-type-values()))
let eventTypeTag = m:tag("event-type", m:taggify(s:get-event-type(.), "unknown", s:event-type-values()))
let tags = $trackerTypeTag + $objectTypeTag + $eventTypeTag

c:check("data_platform.data_collector", "provider_id_not_null", c:check-not-null(fallback(.provider."@id", .provider._AT_id)), $tags, "blocker")
+
c:check("data_platform.data_collector", "schema_url_valid", c:check-schema-url(.schema), $tags, "blocker")
+
c:check("data_platform.data_collector", "deploystage_valid", c:check-one-of(.deployStage, ["dev", "pre", "pro", null]), $tags, "blocker")
```

### Others 

| Function | Description |
| :------- | :---------- |
| `check-schema-url` | Checks the given URL matches an Adevinta/Schibsted schema URL |
| `check-adevinta-schema-url` | Checks the given URL matches an Adevinta schema URL |
| `check-schibsted-schema-url` | Checks the given URL matches an Schibsted schema URL |
| `check-date-format` | Date and time formatted according to Activity Streams 2.0: https://www.w3.org/TR/activitystreams-core/#dates |
| `check-timestamp-format` | Just like `check-date-format`, but forces UTC+00:00 time |
| `check-uuid-v4` | Checks the given value matches UUID v4 format, _ie_: `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx` |
| `check-ip` | Checks the given value matches an IPv4 in dot-decimal notation. |
| `check-email` | Checks the given value matches regex `^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$` |
| `check-null` | Checks the given value is null |
| `check-not-null` | Checks the given value is not null |
| `check-empty` | Checks the given value is empty ([], {}, "", null value is NOT empty) |
| `check-not-empty` | Checks the given value is not empty ([], {}, "", null value is NOT empty) |
| `check-not-null-and-not-empty` | Checks the given value is not empty ([], {}, "", null value is NOT empty) and not null too |
| `check-one-of` | Checks the given value is one of the given ones |
| `check-not-one-of` | Checks the given value is not one of the given ones |
| `check-all` | Checks all values are `true` |
| `check-any` | Checks at least one value is `true` |
| `check-none` | Checks no value is `true` |
| `check-sdrn-account-id` | Checks the given value matches an SDRN account id `^sdrn:([^:]+):user:(.*)$` |
| `check-sdrn-env-id` | Checks the given value matches an SDRN environment id `^sdrn:schibsted:environment:(.*)$` (null env id `'00000000-0000-4000-8000-000000000000'` is also accepted) |
| `check-sdrn-classified-ad` | Checks the given value matches an SDRN classified ad `^sdrn:([^:]+):classified:(.*)$` |
| `check-sdrn-listing` | Checks the given value matches an SDRN listing `^sdrn:([^:]+):listing:(.*)$` |
| `check-sdrn-form` | Checks the given value matches an SDRN form `^sdrn:([^:]+):form:(.*)$` |
| `check-sdrn-message` | Checks the given value matches an SDRN message `^sdrn:([^:]+):message:(.*)$` |
| `check-sdrn-phonecontact` | Checks the given value matches an SDRN phonecontact `^sdrn:([^:]+):phonecontact:(.*)$` |
| `check-sdrn-contactform` | Checks the given value matches an SDRN contactform `^sdrn:([^:]+):contact:(.*)$` |
| `check-sdrn-webpage` | Checks the given value matches an SDRN webpage `^sdrn:([^:]+):(frontpage|page|content):(.*)$` |
| `check-sdrn-provider` | Checks the given value matches an SDRN provider `^sdrn:schibsted:client:.+$` |
| `check-sdrn-conversation` | Checks the given value matches an SDRN conversation `^sdrn:[^:]+:conversation:.+$` |
| `check-sdrn-delivery` | Checks the given value matches an SDRN delivery `^sdrn:([^:]+):delivery:(.*)$` |
| `check-mediaasset-category` | Checks thee given value matches an SDRN mediaaaset category, _ie_: `category > subcategory > etc` |
| `check-number-gt-0` | Checks the given value is a number > 0 |
| `check-number-ge-0` | Checks the given value is a number >= 0 |
| `check-geocoordinate` | Checks the given value is a valid latitude or longitude |
| `no-check` | Syntax sugar for an empty check list. |
| `taggify-event-type` | Retrieves the event tag from an event using the `taggify` method from `lib/metrics.jslt`|

## `checks/core-tagging-plan`

DQC suites based on [Insights' core tagging plan](https://docs.mpi-internal.com/data-and-insight/insights-docs/10.Tagging%20Guide/tagging-plans/10.core-events/).

| Checks | Tagging plan |
| :------- | :---------- |
| `classified-ad-view` | [Ad detail viewed](https://docs.mpi-internal.com/data-and-insight/insights-docs/10.Tagging%20Guide/tagging-plans/10.core-events/ad-detail-viewed/) |

## `checks/p10n`

DQC suites based on Personalisation and [Recommendation](https://docs.mpi-internal.com/data-and-insight/insights-docs/10.Tagging%20Guide/tagging-plans/recommendation/) taggin plans.

| Checks | Tagging plan |
| :------- | :---------- |
| `classified-ad-interactions` | [Core Events for Algorithms](https://docs.mpi-internal.com/p10n/p10n-recsys-user-recs-api/data-integration/user-events/) |
| `click-recommender-event` | [Recommendation Widget Clicked](https://docs.mpi-internal.com/data-and-insight/insights-docs/10.Tagging%20Guide/tagging-plans/recommendation/recommendation-widget-clicked/) |
| `impression-view-recommender-event` | [Recommendation Widget Viewable Impression](https://docs.mpi-internal.com/data-and-insight/insights-docs/10.Tagging%20Guide/tagging-plans/recommendation/recommendation-widget-viewable-impression/) |
| `leads-event` | [Core Events for Algorithms](https://docs.mpi-internal.com/p10n/p10n-recsys-user-recs-api/data-integration/user-events/) |

## `checks/data-platform`

Data Quality Checks in the context of Datahub's Data Platform.

* `checks/data-platform/data-collector` Checks validating the [Data Collector tagging plan](https://docs.mpi-internal.com/yotta/docs/docs/04-guides/03-Tracking/MinimunRequirements/).
* `checks/data-platform/firehose` Different metrics at `Firehose` level. `Firehose` is the entry point for the streaming pipeline in the Data Platform. Metrics include:
  * counters tagged by: event type, object type, event and object type, device type, provider, tracker, ...
  * counter from estimation of Google-bot-generated traffic
