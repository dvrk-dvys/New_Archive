package com.adevinta.data.jslt.lib

import com.adevinta.data.jslt.test.JsltSuite
import org.junit.runner.RunWith
import org.scalatest.Suites
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class JsltLibSuite extends Suites(JsltSuite.suitesFromResources(JsltLibSuite.resourcesPath, NativeFunctionsLib.testFunctions): _*)

object JsltLibSuite {
  private def getListOfSubDirectories(directoryName: String): List[String] = {
    import java.nio.file.Paths
    import java.io.File
    val resourceDirectory = Paths.get("src", "test", "resources")
    val absolutePath = resourceDirectory.toFile.getAbsolutePath
    val dirs = new File("%s/%s".format(absolutePath, directoryName))
      .listFiles
      .filter(_.isDirectory)
      .map(dir => "%s/%s/".format(directoryName, dir.getName)).toList
    dirs ++ dirs.flatMap(dir => getListOfSubDirectories(dir))
  }


  private def getAllTestRessources(): List[String] = {
    val res = getListOfSubDirectories(".")
    println("==== Testing the following directories : %s ====".format(res.toString))
    res
  }

  val resourcesPath = getAllTestRessources()
}
