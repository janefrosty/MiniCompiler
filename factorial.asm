section .text
    global main
    extern malloc
    extern printf
    extern free

factorial:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov eax, dword [rbp-16]
    mov dword [rbp-8], eax
    mov dword [rbp-24], 1
    mov eax, dword [rbp-8]
    mov dword [rbp-32], eax
    cmp dword [rbp-32], 0
    je L1
    mov eax, dword [rbp-40]
    jmp .return_label
    jmp L2
L1:
L2:
    mov eax, dword [rbp-16]
    mov dword [rbp-48], eax
    mov eax, dword [rbp-48]
    imul eax, dword [rbp-64]
    mov dword [rbp-56], eax
    mov eax, dword [rbp-56]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov eax, dword [rbp-16]
    mov dword [rbp-8], eax
    mov eax, dword [rbp-8]
    mov dword [rbp-24], eax
    mov eax, dword [rbp-24]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

section .data
    format db "%d", 10, 0