-- Insert countries
INSERT INTO countries (id, name) VALUES ('5f5e4e94-7d1f-4141-ad47-fae124913010', 'Namibia');
INSERT INTO countries (id, name) VALUES ('45fa8e9c-f8cd-42e4-9e78-919db4181541', 'Kenya');
INSERT INTO countries (id, name) VALUES ('de99b852-f223-4ede-b620-31f2d408deab', 'Uganda');
INSERT INTO countries (id, name) VALUES ('519e9b4e-275c-4d13-b372-ce8249a0931b', 'Tanzania');
INSERT INTO countries (id, name) VALUES ('a8267090-506f-4e94-a94e-1c1b7aa0b6be', 'Nigeria');
INSERT INTO countries (id, name) VALUES ('933d9ad5-4802-46e6-83e7-1cdc47db4fd6', 'Zambia');
INSERT INTO countries (id, name) VALUES ('a16524d7-dc99-4631-b35e-5716a74bd6d6', 'Zimbabwe');
INSERT INTO countries (id, name) VALUES ('744d52a2-1cf7-4e18-b9be-7cd15c9617fa', 'Malawi');
INSERT INTO countries (id, name) VALUES ('dabe1f7a-cfbd-451a-abd6-f18ab1701cb4', 'Mozambique');
INSERT INTO countries (id, name) VALUES ('238117b2-75b5-4071-93ee-6c2832b67b07', 'Angola');
INSERT INTO countries (id, name) VALUES ('e7005c76-d196-4d3d-a94a-9313fc97e253', 'Botswana');

-- Insert clubs
INSERT INTO clubs (name, country_id) VALUES ('Atalanta', '5f5e4e94-7d1f-4141-ad47-fae124913010');
INSERT INTO clubs (name, country_id) VALUES ('Benevento', '5f5e4e94-7d1f-4141-ad47-fae124913010');
INSERT INTO clubs (name, country_id) VALUES ('Bologna', 'de99b852-f223-4ede-b620-31f2d408deab');
INSERT INTO clubs (name, country_id) VALUES ('Cagliari', 'de99b852-f223-4ede-b620-31f2d408deab');
INSERT INTO clubs (name, country_id) VALUES ('Chievo', '519e9b4e-275c-4d13-b372-ce8249a0931b');
INSERT INTO clubs (name, country_id) VALUES ('Crotone', '519e9b4e-275c-4d13-b372-ce8249a0931b');
INSERT INTO clubs (name, country_id) VALUES ('Fiorentina', 'a8267090-506f-4e94-a94e-1c1b7aa0b6be');
INSERT INTO clubs (name, country_id) VALUES ('Genoa', 'a8267090-506f-4e94-a94e-1c1b7aa0b6be');
INSERT INTO clubs (name, country_id) VALUES ('Hellas Verona', '933d9ad5-4802-46e6-83e7-1cdc47db4fd6');
INSERT INTO clubs (name, country_id) VALUES ('Inter', '933d9ad5-4802-46e6-83e7-1cdc47db4fd6');
INSERT INTO clubs (name, country_id) VALUES ('Juventus', 'a16524d7-dc99-4631-b35e-5716a74bd6d6');
INSERT INTO clubs (name, country_id) VALUES ('Lazio', 'a16524d7-dc99-4631-b35e-5716a74bd6d6');
INSERT INTO clubs (name, country_id) VALUES ('Milan', '744d52a2-1cf7-4e18-b9be-7cd15c9617fa');
INSERT INTO clubs (name, country_id) VALUES ('Napoli', '744d52a2-1cf7-4e18-b9be-7cd15c9617fa');
INSERT INTO clubs (name, country_id) VALUES ('Roma', 'dabe1f7a-cfbd-451a-abd6-f18ab1701cb4');
INSERT INTO clubs (name, country_id) VALUES ('Sampdoria', 'dabe1f7a-cfbd-451a-abd6-f18ab1701cb4');
INSERT INTO clubs (name, country_id) VALUES ('Sassuolo', '238117b2-75b5-4071-93ee-6c2832b67b07');
INSERT INTO clubs (name, country_id) VALUES ('SPAL', '238117b2-75b5-4071-93ee-6c2832b67b07');
INSERT INTO clubs (name, country_id) VALUES ('Torino', 'e7005c76-d196-4d3d-a94a-9313fc97e253');
INSERT INTO clubs (name, country_id) VALUES ('Udinese', 'e7005c76-d196-4d3d-a94a-9313fc97e253');
INSERT INTO clubs (name, country_id) VALUES ('Venezia', '5f5e4e94-7d1f-4141-ad47-fae124913010');
INSERT INTO clubs (name, country_id) VALUES ('Verona', '45fa8e9c-f8cd-42e4-9e78-919db4181541');
INSERT INTO clubs (name, country_id) VALUES ('Vicenza', 'de99b852-f223-4ede-b620-31f2d408deab');
INSERT INTO clubs (name, country_id) VALUES ('Virtus Entella', '519e9b4e-275c-4d13-b372-ce8249a0931b');
INSERT INTO clubs (name, country_id) VALUES ('Virtus Lanciano', 'a8267090-506f-4e94-a94e-1c1b7aa0b6be');

-- Insert positions
INSERT INTO positions (id, name, abbrev) VALUES ('6b7703eb-9774-43c8-ae01-2d5aeea33951', 'Goalkeeper', 'GK');
INSERT INTO positions (id, name, abbrev) VALUES ('7873c9f6-a831-446f-b893-4bca17c48d81', 'Left Back', 'LB');
INSERT INTO positions (id, name, abbrev) VALUES ('cc6a1e24-a72b-4781-a6d2-20d85c91465a', 'Right Back', 'RB');
INSERT INTO positions (id, name, abbrev) VALUES ('e3ed4922-12e5-4eee-b620-a4bb7b1b6c87', 'Left Wing Back', 'LWB');
INSERT INTO positions (id, name, abbrev) VALUES ('6b96340d-3ad1-489f-b7db-6d485aa76217', 'Right Wing Back', 'RWB');
INSERT INTO positions (id, name, abbrev) VALUES ('81f81e52-3167-4fbb-87cb-2547eeb0bc6f', 'Left Midfielder', 'LM');
INSERT INTO positions (id, name, abbrev) VALUES ('7ee358eb-a404-4d1f-b67b-3691c8259a88', 'Right Midfielder', 'RM');
INSERT INTO positions (id, name, abbrev) VALUES ('edfb21c3-b558-4db4-8733-fb8d12379a42', 'Left Winger', 'LW');
INSERT INTO positions (id, name, abbrev) VALUES ('cbe019da-d646-4db1-bd78-f8b494a93e6c', 'Right Winger', 'RW');
INSERT INTO positions (id, name, abbrev) VALUES ('5b81e0a3-6d42-4405-9b83-8985e206557a', 'Centre Back', 'CB');
INSERT INTO positions (id, name, abbrev) VALUES ('7cd9965b-3000-47e9-afbc-086f76054368', 'Central Midfielder', 'CM');
INSERT INTO positions (id, name, abbrev) VALUES ('5ac54cea-145b-4ef8-a594-c75e6d3a965f', 'Central Attacking Midfielder', 'CAM');
INSERT INTO positions (id, name, abbrev) VALUES ('2aceb53f-4acd-446a-8a2d-c6b64bfc535e', 'Central Defensive Midfielder', 'CDM');
INSERT INTO positions (id, name, abbrev) VALUES ('d64ba5c8-4c95-407b-a8cf-d245c939d7cd', 'Centre Forward', 'CF');
INSERT INTO positions (id, name, abbrev) VALUES ('8a7c59c8-3f0e-4f13-90f6-0b314a5a6a4a', 'Striker', 'ST');

-- Insert scouts
INSERT INTO scouts (id, name) VALUES ('30366fe1-4c7e-4b0a-9e6d-b9fba0cfdb4a', 'Nkatha Mwendwa');
INSERT INTO scouts (id, name) VALUES ('712cd9a5-0d2c-4d41-832b-1de3fa11029d', 'Thabo Mogotsi');
INSERT INTO scouts (id, name) VALUES ('fcf8dc5e-8760-421b-a832-527c6f595276', 'Thando Magolego');
INSERT INTO scouts (id, name) VALUES ('aafdc38b-2b7f-474e-aace-d00d37c3506c', 'Nyasha Chikowore');
INSERT INTO scouts (id, name) VALUES ('c013c940-4b67-4147-b35e-cce8f20b7406', 'Tawanda Magolego');
INSERT INTO scouts (id, name) VALUES ('80cf1a0e-0f54-497b-81a8-508929522e00', 'Thabo Letsholonyane');
INSERT INTO scouts (id, name) VALUES ('b5d35f68-d6f3-4a1c-881f-f1b2729dd68e', 'John Letsoalo');
INSERT INTO scouts (id, name) VALUES ('01218a4b-13a3-4082-b4d8-d41fe45e569b', 'Julius Letsoalo');
INSERT INTO scouts (id, name) VALUES ('604b2e54-daf4-4d9c-b194-0d8e5d40b9b5', 'Thokozani Khumalo');
INSERT INTO scouts (id, name) VALUES ('c01f8a2c-4d0b-4c6f-8ef4-58cc20650c37', 'Siya Mbuli');

-- Insert players
INSERT INTO players (id, name, position_id, club_id) VALUES ('c29743e3-24ae-4ed7-a4f3-d64ad74dcb47', 'Gianluigi Donnarumma', '6b7703eb-9774-43c8-ae01-2d5aeea33951', '5f5e4e94-7d1f-4141-ad47-fae124913010');
INSERT INTO players (id, name, position_id, club_id) VALUES ('c11c48c9-b260-4a4f-8b93-d643d7cc4bff', 'Theo Hernandez', '7873c9f6-a831-446f-b893-4bca17c48d81', 'de99b852-f223-4ede-b620-31f2d408deab');
INSERT INTO players (id, name, position_id, club_id) VALUES ('08055897-0708-4722-9d7f-614f149d4cfb', 'Davide Calabria', 'cc6a1e24-a72b-4781-a6d2-20d85c91465a', '519e9b4e-275c-4d13-b372-ce8249a0931b');
INSERT INTO players (id, name, position_id, club_id) VALUES ('d3e7e6b1-b7d8-43c5-88a1-10dfdd1d5cd0', 'Fikayo Tomori', '5b81e0a3-6d42-4405-9b83-8985e206557a', 'a8267090-506f-4e94-a94e-1c1b7aa0b6be');
INSERT INTO players (id, name, position_id, club_id) VALUES ('d0134b87-e007-47ef-95be-d16dd9c9b2f2', 'Simon Kjaer', '5b81e0a3-6d42-4405-9b83-8985e206557a', '933d9ad5-4802-46e6-83e7-1cdc47db4fd6');
INSERT INTO players (id, name, position_id, club_id) VALUES ('2d0f4a22-86d6-455e-8833-04e66cdd492f', 'Franck Kessie', '2aceb53f-4acd-446a-8a2d-c6b64bfc535e', 'a16524d7-dc99-4631-b35e-5716a74bd6d6');
INSERT INTO players (id, name, position_id, club_id) VALUES ('014409a7-80b6-4e99-9458-1ae1e78e4d38', 'Sandro Tonali', '2aceb53f-4acd-446a-8a2d-c6b64bfc535e', '744d52a2-1cf7-4e18-b9be-7cd15c9617fa');
INSERT INTO players (id, name, position_id, club_id) VALUES ('af3d4b78-7b5a-493f-93c6-8a32eb45ed23', 'Ismael Bennacer', '7cd9965b-3000-47e9-afbc-086f76054368', 'dabe1f7a-cfbd-451a-abd6-f18ab1701cb4');
INSERT INTO players (id, name, position_id, club_id) VALUES ('6230b482-9c2d-4f70-95f5-1a03d194c540', 'Brahim Diaz', '5ac54cea-145b-4ef8-a594-c75e6d3a965f', '238117b2-75b5-4071-93ee-6c2832b67b07');
INSERT INTO players (id, name, position_id, club_id) VALUES ('abf1d5e3-cd02-44c0-8429-45a5b1c85f3d', 'Rafael Leao', 'edfb21c3-b558-4db4-8733-fb8d12379a42', '5f5e4e94-7d1f-4141-ad47-fae124913010');
INSERT INTO players (id, name, position_id, club_id) VALUES ('2549da6f-b7c3-49af-82a2-022769d3b4f7', 'Zlatan Ibrahimovic', '8a7c59c8-3f0e-4f13-90f6-0b314a5a6a4a', '45fa8e9c-f8cd-42e4-9e78-919db4181541');
