# Без добавления в кликхаус, т.е. только генерация фейковых данных

### CHUNK_SIZE: 10 ** 2
добавлено points: 11_066_000
load_data:
 max_memory: 0.044 mb
 exec time: 31 s

### CHUNK_SIZE: 10 ** 3
добавлено points: 11_066_000
load_data:
 max_memory: 0.331 mb
 exec time: 33 s

### CHUNK_SIZE: 10 ** 4
добавлено points: 11_066_000
load_data:
 max_memory: 3.196 mb
 exec time: 35 s

### CHUNK_SIZE: 10 ** 5
добавлено points: 11_066_000
load_data:
 max_memory: 19.651 mb
 exec time: 36 s

### CHUNK_SIZE: 10 ** 6
добавлено points: 11_066_000
load_data:
 max_memory: 196.276 mb
 exec time: 37 s
--
добавлено points: 111_168_000
load_data:
 max_memory: 196.277 mb
 exec time: 385 s

---------------------------------------------------------------------------------------------------

# Добавляем в кликхаус в пустую бызу:

## Синхронно


### CHUNK_SIZE: 10 ** 2


### CHUNK_SIZE: 10 ** 3


### CHUNK_SIZE: 10 ** 4
добавлено points: 111_168_000
load_data:
 max_memory: 9.644 mb
 exec time: 10,177 s


### CHUNK_SIZE: 10 ** 5
добавлено points: 111_168_000
load_data:
 max_memory: 35.664 mb
 exec time: 1,691 s

### CHUNK_SIZE: 10 ** 6
добавлено points: 111_168_000
load_data:
 max_memory: 295.692 mb
 exec time: 1,486 s

### CHUNK_SIZE: 10 ** 7
добавлено points: 111_168_000
load_data:
 max_memory: 310.074 mb
 exec time: 1,444 s

---------------------------------------------------------------------------------------------------

## АСинхронно
points: 111_168_000

### CHUNK_SIZE: 10 ** 4
async_2

### CHUNK_SIZE: 10 ** 5
CHUNK_SIZE: 100000
finished in 959 second(s)

async_2
2 попытка
369, 862.14
372, 863.66
371, 857.18
in 1040 second(s)
### CHUNK_SIZE: 10 ** 6
### CHUNK_SIZE: 10 ** 7


10 ** 3
1. finished in 5814.80 sec

10 ** 4
1. finished in 1103.55 sec
2. finished in 1145.47 sec
shard_1: 5412, 873.970
shard_2: 5404, 871.791

10 ** 5
1. finished in 994.21 sec
2. finished in 1006.90 sec
shard_1: 371, 831.971
shard_2: 371, 831.730
shard_3: 370, 829.163

10 ** 5 * 2
1. finished in 997.72 sec
2. finished in 1001.72 sec
shard_1: 186, 828.575
shard_2: 185, 828.651
shard_3: 185, 826.042


# Vertica

points: 11_066_000

10 ** 2
time: 5917.92 sec

10 ** 3
time: 636.69 sec

10 ** 4
time: 290.75 sec


points: 111_168_000
10 ** 4
time: 2923.97

10 ** 5
time: 2535.29

10 ** 6
time: 2502.41

10 ** 7
time: 