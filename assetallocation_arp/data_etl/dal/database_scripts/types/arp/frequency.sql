DROP TYPE IF EXISTS  arp.frequency CASCADE;
CREATE TYPE arp.frequency AS ENUM ('daily', 'weekly', 'monthly');