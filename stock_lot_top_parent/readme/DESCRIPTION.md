This module adds top-level parent traceability fields to lots/serials
(*Inventory > Products > Lots/Serial Numbers*):

- **Top lv Parent S/N**: the serial number (lot) of the top-level parent
  assembly this lot belongs to.
- **Top lv Parent P/N**: the product of the top-level parent serial
  (a related field, kept in sync automatically).
- **Physical Location**: the current internal location(s) of the top-level
  parent serial, computed on the fly from stock quants. It is empty when
  the parent serial is not stored in any internal location.
