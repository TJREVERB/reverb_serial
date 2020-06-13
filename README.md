Project Description
-------------------

**this package is only meant for use within the TJREVERB pFS codebase**

*use of this package in other projects is not supported and not advised*

reverb-serial is a custom serial library meant for use with the Simulator
testing suite. Instead of conducting actual serial calls to physical
hardware, reverb-serial will save all data to a local text file which then
can be read by the Simulator. More information on Simulator
`here <https://github.com/TJREVERB/software-in-the-loop.git>`__.

Since this package is meant to override the conventional ``pyserial``
package, reverb-serial **MUST** be installed in a separate virtual
environment.

Quick Start Testing
-------------------

To install this package:

``pip install reverb-serial``

* The conventional pyserial package, if present will be overridden by installing this package
