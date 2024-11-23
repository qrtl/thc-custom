This module adds the related_valuation_layer_ids field, which links all the related
SVL records including self (i.e. origin SVL that links to a stock move, plus adjustment
SVLs).

The added field can, for example, be used in the configuration of some server actions
with navigate action, which is enabled with the OCA module server_action_navigate.
