import random

# Função para encontrar um gerador primitivo de um número primo
def find_primitive_root(p):
    """
    Encontra uma raiz primitiva para um número primo p.
    
    p: O número primo.
    phi: O valor de p - 1.
    factors: Um conjunto de fatores de phi.
    
    A função testa números de 2 a p-1 para encontrar uma raiz primitiva r.
    """
    if p == 2:
        return 1
    phi = p - 1
    factors = set()
    n = phi
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factors.add(n)
    
    for r in range(2, p):
        is_primitive = True
        for factor in factors:
            if pow(r, phi // factor, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return r
    return None

# Função para gerar chaves pública e privada
def generate_keys(p, g):
    """
    Gera uma chave privada e uma chave pública.
    
    p: O número primo.
    g: A raiz primitiva.
    private_key: A chave privada escolhida aleatoriamente entre 1 e p-2.
    public_key: A chave pública calculada como g^private_key % p.
    """
    private_key = random.randint(1, p - 2)
    public_key = pow(g, private_key, p)
    return private_key, public_key

# Função para criptografar uma mensagem
def encrypt(p, g, public_key, plaintext):
    """
    Criptografa uma mensagem usando a chave pública.
    
    p: O número primo.
    g: A raiz primitiva.
    public_key: A chave pública da outra parte.
    plaintext: A mensagem a ser criptografada (representada como um número).
    k: Um valor aleatório escolhido para cada criptografia.
    c1: A chave efêmera calculada como g^k % p.
    c2: A mensagem cifrada calculada como plaintext * public_key^k % p.
    ciphertext: O par (c1, c2).
    """
    k = random.randint(1, p - 2)
    c1 = pow(g, k, p)
    c2 = (plaintext * pow(public_key, k, p)) % p
    return c1, c2

# Função para descriptografar uma mensagem
def decrypt(p, private_key, ciphertext):
    """
    Descriptografa uma mensagem usando a chave privada.
    
    p: O número primo.
    private_key: A chave privada.
    ciphertext: O par (c1, c2).
    s: O valor calculado como c1^private_key % p.
    s_inv: O inverso modular de s calculado usando a propriedade de Fermat.
    plaintext: A mensagem original recuperada como c2 * s_inv % p.
    """
    c1, c2 = ciphertext
    s = pow(c1, private_key, p)
    s_inv = pow(s, p - 2, p)  # Usando a propriedade de Fermat para inverso modular
    plaintext = (c2 * s_inv) % p
    return plaintext

# Exemplo de uso
if __name__ == "__main__":
    """
    Exemplo de uso:
    
    - Escolha de um número primo grande p e uma raiz primitiva g.
    - Geração de chaves pública e privada.
    - Criptografia de uma mensagem.
    - Descriptografia da mensagem.
    - Verificação de que a mensagem descriptografada coincide com a original.
    """
    # Escolher um número primo grande p
    p = 23  # Este é um exemplo, na prática, p deve ser um primo muito grande
    # Encontrar uma raiz primitiva g para p
    g = find_primitive_root(p)

    print(f"Número primo (p): {p}")
    print(f"Raiz primitiva (g): {g}")

    # Geração das chaves
    private_key, public_key = generate_keys(p, g)
    print(f"Chave privada: {private_key}")
    print(f"Chave pública: {public_key}")

    # Mensagem a ser criptografada (representada como um número)
    plaintext = 15  # A mensagem deve ser um número no intervalo [0, p-1]
    print(f"Mensagem original: {plaintext}")

    # Criptografar a mensagem
    ciphertext = encrypt(p, g, public_key, plaintext)
    print(f"Mensagem criptografada: {ciphertext}")

    # Descriptografar a mensagem
    decrypted_message = decrypt(p, private_key, ciphertext)
    print(f"Mensagem descriptografada: {decrypted_message}")

    # Verificação
    assert plaintext == decrypted_message, "A mensagem descriptografada não coincide com a mensagem original!"
    print("A mensagem foi descriptografada corretamente.")
