
# Type: node obsoletion with split


An obsoletion change in which information from the obsoleted node is moved selectively to multiple targets

URI: [ocl:NodeObsoletionWithSplit](http://w3id.org/oclNodeObsoletionWithSplit)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NodeObsoletion]^-[NodeObsoletionWithSplit&#124;about(i):string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F])

## Parents

 *  is_a: [NodeObsoletion](NodeObsoletion.md)

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
