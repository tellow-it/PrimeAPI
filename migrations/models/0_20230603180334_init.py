from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "building" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "building_name" VARCHAR(200) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "important" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "important_name" VARCHAR(200) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "status" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status_name" VARCHAR(200) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "system" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "system_name" VARCHAR(200) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "surname" VARCHAR(100) NOT NULL,
    "role" VARCHAR(13) NOT NULL,
    "password" VARCHAR(200) NOT NULL,
    "telephone" VARCHAR(11) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user"."role" IS 'admin: admin\nuser: user\nadvanced_user: advanced_user';
CREATE TABLE IF NOT EXISTS "order" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "material" TEXT NOT NULL,
    "quantity" INT NOT NULL,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "expected_time" TIMESTAMPTZ,
    "building_id" INT NOT NULL REFERENCES "building" ("id") ON DELETE CASCADE,
    "creator_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "important_id" INT NOT NULL REFERENCES "important" ("id") ON DELETE CASCADE,
    "status_id" INT NOT NULL REFERENCES "status" ("id") ON DELETE CASCADE,
    "system_id" INT NOT NULL REFERENCES "system" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
