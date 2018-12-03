
CREATE TABLE "producttype" (
  "nameproducttype" VARCHAR(255) NOT NULL UNIQUE,
  "unit" VARCHAR(255) NOT NULL,
  CONSTRAINT producttype_pk PRIMARY KEY ("nameproducttype")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "orderitems" (
  "idorderitems" INTEGER NOT NULL,
  "amount" INTEGER NOT NULL,
  "priceorderitems" INTEGER NOT NULL,
  "idorders" INTEGER NOT NULL,
  "idproduct" INTEGER NOT NULL,
  CONSTRAINT orderitems_pk PRIMARY KEY ("idorderitems")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "product" (
  "idproduct" INTEGER NOT NULL,
  "nameproduct" VARCHAR(255) NOT NULL,
  "priceproduct" INTEGER NOT NULL,
  "img" VARCHAR(255),
  "nameproducttype" VARCHAR(255) NOT NULL,
  CONSTRAINT product_pk PRIMARY KEY ("idproduct")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "orders" (
  "idorders" INTEGER NOT NULL,
  "payment" BOOL NOT NULL,
  "status" BOOL NOT NULL,
  "price" INTEGER NOT NULL,
  "idusers" INTEGER NOT NULL,
  CONSTRAINT orders_pk PRIMARY KEY ("idorders")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "users" (
  "idusers" INTEGER,
  "admin" BOOL NOT NULL,
  "email" VARCHAR(255) NOT NULL,
  "password" VARCHAR(255) NOT NULL,
  CONSTRAINT users_pk PRIMARY KEY ("idusers")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "orderitems" ADD CONSTRAINT "orderitems_fk0" FOREIGN KEY ("idorders") REFERENCES "orders"("idorders");
ALTER TABLE "orderitems" ADD CONSTRAINT "orderitems_fk1" FOREIGN KEY ("idproduct") REFERENCES "product"("idproduct");

ALTER TABLE "product" ADD CONSTRAINT "product_fk0" FOREIGN KEY ("nameproducttype") REFERENCES "producttype"("nameproducttype");

ALTER TABLE "orders" ADD CONSTRAINT "orders_fk0" FOREIGN KEY ("idusers") REFERENCES "users"("idusers");
