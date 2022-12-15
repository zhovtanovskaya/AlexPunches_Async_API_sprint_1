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

### CHUNK_SIZE: 10 ** 4
### CHUNK_SIZE: 10 ** 5
CHUNK_SIZE: 100000
готово points: 111_168_000
finished in 959.1712 second(s)
### CHUNK_SIZE: 10 ** 6
### CHUNK_SIZE: 10 ** 7