# Cable replication and manufacturing package — v0.1

Status: **active preservation workstream**

Date: 2026-11-18

## 1. Preservation decision

The original Seiko TV Watch cable is treated as an irreplaceable historical reference part.

**The original cable will not be sent to a manufacturer, sacrificed, cut, opened, desoldered, stripped, or used as a destructive reverse-engineering sample.**

All replication work must be based on non-destructive measurement and documentation generated from the original.

The preferred manufacturing route is **build from drawings/CAD**, not “copy this physical sample”.

## 2. Scope

The target is a functionally interchangeable cable between the original receiver and wristwatch, while leaving both original devices unmodified.

The reproduction must preserve:

- connector geometry on both ends;
- contact orientation and numbering;
- pin-to-pin continuity;
- cable diameter and flexibility;
- strain relief;
- connector retention/locking geometry;
- any shield or chassis contact, if confirmed;
- adequate conductor gauge and insulation.

## 3. Current electrical baseline

The project working reconstruction currently uses a six-conductor interface plus a possible additional chassis contact:

| Pin | Working function | Status |
|---|---|---|
| 1 | ~8.9 V supply | verify on original |
| 2 | ~13.2 V supply | verify on original |
| 3 | ~4.1 V supply | verify on original |
| 4 | electrical ground | working confirmed function |
| 5 | composite sync / VID1 | levels and impedance still to characterize |
| 6 | analog video / VID2 with DC bias | transfer and impedance still to characterize |
| extra contact | possible chassis ground | relationship to pin 4 to verify |

For cable replication, the important requirement is an unambiguous physical pin map and continuity map. Electrical function knowledge is useful but not required to manufacture a passive 1:1 cable once the mechanical and continuity data are frozen.

## 4. Non-destructive measurement set

Before freezing Rev A, record:

- total cable length between defined datum points;
- cable outer diameter;
- connector width, height and depth;
- insertion depth;
- contact pitch;
- contact width/thickness where measurable;
- position of contacts relative to mechanical datums;
- latch, guide and key geometry;
- radii and chamfers;
- strain-relief geometry;
- pin-to-pin continuity;
- continuity between chassis/mechanical contact and electrical ground;
- approximate resistance of each conductor;
- presence/absence of shielding;
- unequivocal physical orientation of pin 1 at both ends.

Use calipers, macro photography and low-energy electrical measurements.

## 5. Manufacturing package

Planned Rev A deliverables:

- `TVWATCH_CABLE_REV_A.pdf` — master dimensioned cable drawing;
- `TVWATCH_CONNECTOR_WATCH.step` — watch-side connector 3D model;
- `TVWATCH_CONNECTOR_RX.step` — receiver-side connector 3D model;
- `TVWATCH_CONNECTORS.dxf` — critical 2D profiles;
- `TVWATCH_WIRE_LIST.csv` — pin-to-pin wire list;
- `TVWATCH_BOM.csv` — cable/contact/housing/material BOM;
- `TVWATCH_TEST_SPEC.pdf` — electrical and dimensional acceptance tests.

These names define the intended package structure; the actual CAD and measured values are not frozen yet.

## 6. Supplier strategy

Search for suppliers that accept custom cable assembly / wire harness / overmolded cable work **from engineering drawings and CAD files**.

Preferred sequence:

1. issue preliminary drawings for manufacturability feedback;
2. request quotation without supplying the original cable;
3. build 2–5 prototypes;
4. validate electrically and mechanically;
5. freeze Rev B or production revision;
6. order a small production run only after prototype acceptance.

If a conventional molded proprietary connector is uneconomic, evaluate:

- high-resolution additive manufacture;
- machined connector body;
- hybrid printed/machined body with commercial or custom contacts;
- low-volume silicone/urethane tooling.

## 7. Prototype acceptance

A prototype passes only if:

- all continuity matches the frozen wire list;
- no unintended shorts exist;
- conductor resistance is within the defined limit;
- connector orientation is correct;
- insertion does not require excessive force;
- retention works correctly;
- no original device modification is required;
- critical dimensions are within tolerance.

Whenever practical, repetitive fit testing should use gauges, fixtures or replicas rather than repeatedly cycling the historical watch connector.

## 8. Next actions

1. Photograph both cable ends orthogonally and in macro.
2. Freeze a physical connector orientation convention.
3. Measure critical dimensions.
4. Capture continuity and chassis-contact relationships.
5. Produce first 2D connector drawings.
6. Produce STEP models.
7. Fill wire list and BOM.
8. Release manufacturing PDF Rev A.
9. Request prototype quotations from drawing/CAD only.

## 9. Repository/Drive role

Git remains the authoritative engineering decision log and versioned design record.

Google Drive remains the documentary backup for historical source material, photographs, measurements and manufacturing-package working files.
