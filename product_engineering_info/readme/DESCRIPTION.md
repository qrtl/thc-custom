This module extends products with engineering-oriented information:

- An **Engineering** tab on the product form gathering the following fields:
  - **Active Flag**: whether the part is still to be ordered (an
    engineering view; distinct from Odoo's archive flag).
  - **Product Group Code**: a design classification (e.g. sheet metal,
    circuit board), managed under *Inventory > Configuration > Products*.
  - **Successor P/N**: the part that supersedes this one.
  - **BOM Link**: a link to the engineering BOM file (separate from Odoo
    BoMs).
  - **Technical Notes**: free-form notes for engineers.
  - **Compatible P/N**: parts usable as substitutes when out of stock.

The tab is also a convenient place for administrators to add further
engineering fields through Studio.
