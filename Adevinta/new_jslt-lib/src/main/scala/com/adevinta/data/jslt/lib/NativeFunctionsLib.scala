package com.adevinta.data.jslt.lib

import com.schibsted.spt.data.jslt.Function

/**
  * Lib of functions natively implemented in Scala.
  */
object NativeFunctionsLib {

  private[this] val functions: Seq[Function] = Seq.empty[Function]

  def testFunctions = functions
}
