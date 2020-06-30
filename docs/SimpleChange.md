
# Type: simple change


A change that is about a single ontology element

URI: [ocl:SimpleChange](http://w3id.org/oclSimpleChange)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SimpleChange&#124;about:string%20%3F;old_value:string%20%3F;new_value:string%20%3F]^-[NodeChange],%20[SimpleChange]^-[EdgeChange])

## Children

 * [EdgeChange](EdgeChange.md)
 * [NodeChange](NodeChange.md)

## Referenced by class


## Attributes


### Inherited from node change:

 * [node change➞about](node_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeChange](NodeChange.md)

### Inherited from node rename:

 * [node rename➞old value](node_rename_old_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)
 * [node rename➞new value](node_rename_new_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)
