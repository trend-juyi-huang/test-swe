{% snapshot dim_aggregated_brand_hierarchy_snapshot %}

{{
    config(
      strategy='check',
      unique_key='c1',
      target_schema='snapshots',
      check_cols='all'
    )
}}

select
    c1
from
    foo

{% endsnapshot %}
