#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/rand.h>

#define KEY_SIZE 32
#define IV_SIZE 16
#define MAX_INPUT_SIZE 65536
#define ENCRYPTED_FILE "encrypted.json"

// random values must repalce placeholders
const unsigned char key[KEY_SIZE] = "01234567890123456789012345678901"; // 32 bytes
const unsigned char iv[IV_SIZE]   = "0123456789012345";                 // 16 bytes

void handleErrors() {
    ERR_print_errors_fp(stderr);
    exit(1);
}

int aes_encrypt(const unsigned char* plaintext, int plaintext_len, unsigned char* ciphertext) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    int len, ciphertext_len;

    EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv);
    EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
    ciphertext_len = len;
    EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
    ciphertext_len += len;

    EVP_CIPHER_CTX_free(ctx);
    return ciphertext_len;
}

int aes_decrypt(const unsigned char* ciphertext, int ciphertext_len, unsigned char* plaintext) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    int len, plaintext_len;

    EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv);
    EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len);
    plaintext_len = len;
    EVP_DecryptFinal_ex(ctx, plaintext + len, &len);
    plaintext_len += len;

    EVP_CIPHER_CTX_free(ctx);
    return plaintext_len;
}

void write_mode() {
    unsigned char input[MAX_INPUT_SIZE];
    size_t read_len = fread(input, 1, MAX_INPUT_SIZE, stdin);
    if (read_len == 0) {
        fprintf(stderr, "No input received\n");
        exit(1);
    }

    unsigned char* encrypted = malloc(read_len + EVP_MAX_BLOCK_LENGTH);
    int enc_len = aes_encrypt(input, read_len, encrypted);

    FILE* fp = fopen(ENCRYPTED_FILE, "wb");
    if (!fp) { perror("fopen"); exit(1); }
    fwrite(encrypted, 1, enc_len, fp);
    fclose(fp);
    free(encrypted);
}

void read_mode() {
    FILE* fp = fopen(ENCRYPTED_FILE, "rb");
    if (!fp) { perror("fopen"); exit(1); }

    fseek(fp, 0, SEEK_END);
    long file_len = ftell(fp);
    rewind(fp);

    unsigned char* encrypted = malloc(file_len);
    fread(encrypted, 1, file_len, fp);
    fclose(fp);

    unsigned char* decrypted = malloc(file_len + EVP_MAX_BLOCK_LENGTH);
    int dec_len = aes_decrypt(encrypted, file_len, decrypted);

    fwrite(decrypted, 1, dec_len, stdout);
    free(encrypted);
    free(decrypted);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s [write|read]\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "write") == 0) {
        write_mode();
    } else if (strcmp(argv[1], "read") == 0) {
        read_mode();
    } else {
        fprintf(stderr, "Unknown command: %s\n", argv[1]);
        return 1;
    }

    return 0;
}
