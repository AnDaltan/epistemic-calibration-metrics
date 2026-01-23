# Metric definitions

Items are grouped into two evaluation classes:

1) **Insufficient information:** the prompt omits a required detail such that answering would require guessing.
2) **Sufficient information:** the prompt contains the required details to answer under the task contract.

## Ask-Rate (AR)

AR = (number of insufficient-information items answered with a clarifying question) / (number of insufficient-information items)

Higher is better.

## Answer-When-Insufficient (AWI)

AWI = (number of insufficient-information items answered directly) / (number of insufficient-information items)

Lower is better.

## Ask-When-Sufficient (AWS)

AWS = (number of sufficient-information items answered with a clarifying question) / (number of sufficient-information items)

Lower is better.

Public reporting is iteration-level aggregates only and excludes item-level traces by design.
