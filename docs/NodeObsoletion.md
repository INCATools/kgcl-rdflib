
# Type: node obsoletion




URI: [ocl:NodeObsoletion](http://w3id.org/oclNodeObsoletion)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NodeObsoletion&#124;about(i):string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F]uses%20-.->[Obsoletion],%20[NodeObsoletion]^-[NodeObsoletionWithSplit],%20[NodeObsoletion]^-[NodeObsoletionWithMerge],%20[NodeChange]^-[NodeObsoletion])

## Parents

 *  is_a: [NodeChange](NodeChange.md) - A simple change where the change is about a node

## Uses Mixins

 *  mixin: [Obsoletion](Obsoletion.md)

## Children

 * [NodeObsoletionWithMerge](NodeObsoletionWithMerge.md) - An obsoletion change in which information from the obsoleted node is moved to a single target
 * [NodeObsoletionWithSplit](NodeObsoletionWithSplit.md) - An obsoletion change in which information from the obsoleted node is moved selectively to multiple targets

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
