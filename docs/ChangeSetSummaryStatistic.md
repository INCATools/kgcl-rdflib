
# Type: change set summary statistic


A summary statistic for a set of changes of the same type, grouped by zero or more node properties

URI: [kgcl:ChangeSetSummaryStatistic](http://w3id.org/kgclChangeSetSummaryStatistic)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[PropertyValue],[PropertyValue]<property%20value%20set%200..*-++[ChangeSetSummaryStatistic&#124;change_type:change_class_type%20%3F;count:integer%20%3F])

## Referenced by class


## Attributes


### Own

 * [change set summary statistic➞change type](change_set_summary_statistic_change_type.md)  <sub>OPT</sub>
    * range: [ChangeClassType](types/ChangeClassType.md)
 * [change set summary statistic➞count](change_set_summary_statistic_count.md)  <sub>OPT</sub>
    * range: [Integer](types/Integer.md)
 * [change set summary statistic➞property value set](change_set_summary_statistic_property_value_set.md)  <sub>0..*</sub>
    * Description: Summary statistic is grouped by these constraints
    * range: [PropertyValue](PropertyValue.md)
