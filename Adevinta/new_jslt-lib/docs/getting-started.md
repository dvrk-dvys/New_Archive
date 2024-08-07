# Getting started

## JSLT

Next some resources to get familiar with [JSLT](https://github.com/schibsted/jslt):

* [Quick reference](https://github.com/schibsted/jslt#quick-reference)
* [Language tutorial](https://github.com/schibsted/jslt/blob/master/tutorial.md)
* [Out-of-the-box functions in JSLT](https://github.com/schibsted/jslt/blob/master/functions.md)
* On-line JSLT playgrounds: [Datahub](https://datahub.mpi-internal.com/audience/playground), 
[Public JSLT](http://spt-data-dev-public-web.s3-website-eu-west-1.amazonaws.com/jstl2.html)

## JSLT-lib

Check existing functions in [JSLT-lib API](API.md)

## Using the library

JSLT-lib is already integrated with some applications in the Data Highway. So functions defined in the library 
became immediately available in those applications.

Of course, users can use the library in their projects by adding the following Gradle dependency:

```
compile "com.adevinta.data:jslt-lib_2.12:0.1.+"
```

Once `JSLT-lib` is in the classpath, all functions defined there will become available. 
You can programatically use them to transform a `JsonNode` as follows:

```scala
import com.schibsted.spt.data.jslt.Parser
import com.schibsted.spt.data.jslt.Expression
import com.fasterxml.jackson.databind.ObjectMapper

val mapper: ObjectMapper = new ObjectMapper()
val inputJson: JsonNode = mapper.readTree("<input json here>")
val inputJslt: String =  "<input jslt here>"
val jslt: Expression = Parser.compileString(inputJslt)
val outputJson: JsonNode = jslt.apply(inputJson)
```

!!! tip "JSLT syntax highlighting extension for VS Code"
    There exists a nice [JSLT syntax highlighting extension](https://marketplace.visualstudio.com/items?itemName=jarno-rajala.jslt-lang) for VS Code.

## Building locally

You can build locally by running:

```bash
$ ./gradlew build
```

Note build process will download dependencies from artifactory.mpi-internal.com, which requires authentication. In the project, gradle picks up credentials from environment, so you can set them as follows:

You'll need to generate an [Artifactory API key](https://artifactory.mpi-internal.com/artifactory/webapp/#/profile) (if you already have one, you can use it)

```
$ cat $HOME/.gradle/gradle.properties 
# MPI-INTERNAL
artifactory_context = https://artifactory.mpi-internal.com/artifactory
artifactory_contextUrl = https://artifactory.mpi-internal.com/artifactory
artifactory_user = <email>@adevinta.com
artifactory_pwd = <artifactory.mpi-internal.com api key>
artifactory_password = <artifactory.mpi-internal.com api key>
```

Also note, artifactory.mpi-internal.com requires Heimdall VPN.

## Running locally from CLI

You can run JSLT locally from CLI to quickly test a transformation.

```bash
jslt-lib (master) $ cat event.json 
{
  "array": [ "a", "b", "c" ]
}
jslt-lib (master) $ cat transformation.jslt 
{
  "array-size" : size(.array)
}
jslt-lib (master) $ ./gradlew -q -PmainClass=com.schibsted.spt.data.jslt.cli.JSLT run --args="transformation.jslt event.json"
{
  "array-size" :
    size(
      .array
    )
}
{
  "array-size" : 3
}
```
