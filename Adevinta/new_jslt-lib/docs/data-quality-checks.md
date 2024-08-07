# Data Quality Checks

## Overview

Data Quality Checks (DQC) are organized in **_Data Quality Check suites_**. Each DQC suite is usually aligned to a 
tagging plan.

Each DQC is a boolean condition to be applied to a given input (usually this input 
corresponds to an event). So the result of any DQC is binary, input passes or not the check. 

Additionaly, DQCs are classified according to its criticality and how data consumer is 
affected in an scenario where inputs are not passsing the checks:

* Blocker. Data consumer cannot operate in these conditions and ceases its functions.
* Critical. Data consumer can operate in these conditions however may cause unexpected or wrong results.
* Minor. This is just a nice to have. Consumer can operate in these conditions with no 
problem, however it is recommended in order to have optimal and accurate results.

Definition of individual DQCs is supported by [`checks` API](API.md#check):

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

So, DQC suites correspond to all those DQC sharing the `check-suite` parameter and enclosed in a `*.jslt` file. 
The file name and the `check-suite` value must match.

## Conventions for automatic integration with DataHub

### File name

DQC suites suffixed with `-suite.jslt` will be automatically available in DataHub.

### Folder structure

DQC suites live in the [checks folder](https://github.mpi-internal.com/yotta/jslt-lib/tree/master/src/main/resources/checks). 
Each folder under `checks` is a _category_. Nested folders are also categories.

```
checks/foo/bar.jslt
Category: foo;
Name: bar

checks/foo/baz/qux.jslt
Category: foo/baz
Name: qux
```

## DQC consumption

### Data Quality metrics and tagging

When applied on a data flow, DQCs become real-time metrics being published in DataDog. 
All DQCs are tracked in the metric **`com.adevinta.data.duratro.metrics.quality.check`**. 
This metric is tagged with the following values got from [`checks` API](API.md#check) so user can perform the drill-down analysis:

* `check-suite`
* `check-name`
* `check-result`: `(true|false)`
* `check-impact`: `(blocker|critical|minor)`
* Key-value pairs in the user-defined `tag-object` become tags in the metric too.

### DataDog

Real-time metrics are published in `SPT Data Analytics DataDog` account.
Please, ask #yotta-team to be member of `gp.es.app.dd.sptdaa.su` google group in order to have access 
to the `SPT Data Analytics DataDog` account as Standard User.

Once published in DataDog, a user can:

* Check out the metrics in the [out-of-the-box general-purpose Data Quality dashboard](https://app.datadoghq.com/dashboard/tvc-keb-rqx/yottadata-quality-data-highway).
* Built their own dashboards
* Set-up monitors (alarms)
