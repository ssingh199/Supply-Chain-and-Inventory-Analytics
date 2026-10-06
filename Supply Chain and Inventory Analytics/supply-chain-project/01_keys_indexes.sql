   USE supply_chain;

   ALTER TABLE dim_customer   ADD PRIMARY KEY (customer_id);
   ALTER TABLE dim_product    ADD PRIMARY KEY (product_card_id);
   ALTER TABLE dim_department ADD PRIMARY KEY (department_id);
   ALTER TABLE dim_date       ADD PRIMARY KEY (date_key);
   ALTER TABLE fact_orders    ADD PRIMARY KEY (order_item_id);

   CREATE INDEX idx_fact_customer   ON fact_orders (customer_id);
   CREATE INDEX idx_fact_product    ON fact_orders (product_card_id);
   CREATE INDEX idx_fact_department ON fact_orders (department_id);
   CREATE INDEX idx_fact_date       ON fact_orders (date_key);

   ALTER TABLE fact_orders
     ADD CONSTRAINT fk_customer   FOREIGN KEY (customer_id)     REFERENCES dim_customer (customer_id),
     ADD CONSTRAINT fk_product    FOREIGN KEY (product_card_id) REFERENCES dim_product (product_card_id),
     ADD CONSTRAINT fk_department FOREIGN KEY (department_id)   REFERENCES dim_department (department_id),
     ADD CONSTRAINT fk_date       FOREIGN KEY (date_key)        REFERENCES dim_date (date_key);