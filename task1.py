import hashlib

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size

    def _hash(self, item, seed):
        hash_obj = hashlib.md5((str(item) + str(seed)).encode('utf-8'))
        return int(hash_obj.hexdigest(), 16) % self.size

    def add(self, item):
        for i in range(self.num_hashes):
            digest = self._hash(item, i)
            self.bit_array[digest] = True

    def contains(self, item):
        for i in range(self.num_hashes):
            digest = self._hash(item, i)
            if not self.bit_array[digest]:
                return False
        return True

def check_password_uniqueness(bloom, passwords):
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password:
            results[password] = "некоректний"
            continue
        
        if bloom.contains(password):
            results[password] = "вже використаний"
        else:
            bloom.add(password)
            results[password] = "унікальний"
            
    return results

if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")