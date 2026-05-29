section .text
    global main
    extern malloc
    extern printf
    extern free

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], 0
L1:
    mov eax, dword [rbp-8]
    mov dword [rbp-16], eax
    mov dword [rbp-24], 10
    mov eax, dword [rbp-16]
    mov dword [rbp-32], eax
    cmp dword [rbp-32], 0
    je L2
    mov eax, dword [rbp-8]
    mov dword [rbp-40], eax
    mov dword [rbp-48], 1
    mov eax, dword [rbp-40]
    add eax, dword [rbp-48]
    mov dword [rbp-56], eax
    mov eax, dword [rbp-56]
    mov dword [rbp-8], eax
    jmp L1
L2:
    mov eax, dword [rbp-8]
    mov dword [rbp-64], eax
    mov eax, dword [rbp-64]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

section .data
    format db "%d", 10, 0