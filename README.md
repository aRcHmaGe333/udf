# Universal Data Fabric (working title)

The same data gets copied everywhere.

Across devices. Across apps. Across servers. Across backups. Across versions where 99% of the thing is still exactly the same.

UDF starts from the question: **why keep moving and storing the same bytes if we already have them?**

The basic idea is simple:

- split data into chunks
- identify those chunks reliably
- store unique chunks once
- reference them wherever they are needed
- when something changes, move the changed chunks instead of the whole thing again
- keep frequently used chunks near where they are actually used

That is the core. Everything else in this repo is an attempt to make that idea useful enough to survive real systems.

## What exists right now

This is R&D, not a finished storage platform.

The repo already has:

- architecture/specification work
- chunk/manifest/locator/cache design
- an impact model
- hardware planning
- pilot and roadmap material
- small Python examples for deduplication, delta sync and caching
- reference-implementation planning

Current stage: **R&D architecture + small executable demonstrations**.

So I am not claiming "we replaced cloud storage." I am claiming there is enough here to test the proposition properly.

## Why this matters

The obvious value is less duplicated storage and less unnecessary network transfer.

That can mean lower storage cost, less bandwidth, faster updates and less hardware/energy spent carrying identical data around for no reason.

The sustainability claim is the same as the technical claim: if you stop storing and moving redundant data, you should waste less infrastructure doing it.

The next useful step is to benchmark that honestly on real workloads and see how much disappears.

## Start here

If you just want to understand the thing:

- [General-audience start](docs/start-here.md)
- [Overview](docs/overview.md)
- [Value examples](docs/value-examples.md)
- [Impact model](docs/impact-model.md)

If you actually want to build/test it:

- [Architecture](docs/architecture.md)
- [Data pillar](docs/pillars/data/architecture.md)
- [Manifest spec](docs/pillars/data/manifest-spec.md)
- [Locator design](docs/pillars/data/locator-design.md)
- [Cache design](docs/pillars/data/cache-design.md)
- [Compute cache](docs/pillars/compute/compute-cache.md)
- [Reference implementation](docs/reference-impl.md)
- [Quickstart](docs/QUICKSTART.md)
- [Pilot plan](docs/pilot-plan.md)

## What I want next

A small reference implementation that is annoying to argue with.

Pick a few real workloads. Measure storage, transfer, latency and energy/hardware implications against the boring baseline. Show exactly where UDF wins, where it does not, and what the tradeoffs cost.

That is much more useful than another 40-page architectural hymn.

If you run infrastructure, storage, edge systems, devices, data platforms or sustainability benchmarking and want to help test this properly, I am interested.

## License

All Rights Reserved. See [LICENSE.txt](LICENSE.txt).

You can view and link to the repository. Copying/modification/redistribution requires permission.

[Support the work](https://ko-fi.com/earthcraft)
