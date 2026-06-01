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
    mov eax, dword [rbp-16]
    mov dword [rbp-56], eax
    mov dword [rbp-64], 1
    mov eax, dword [rbp-56]
    sub eax, dword [rbp-64]
    mov dword [rbp-72], eax
    mov dword [rbp-80], 0
    mov eax, dword [rbp-48]
    imul eax, dword [rbp-80]
    mov dword [rbp-88], eax
    mov eax, dword [rbp-88]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], 6
    mov dword [rbp-16], 0
    mov eax, dword [rbp-16]
    mov dword [rbp-24], eax
    mov eax, dword [rbp-24]
    mov dword [rbp-32], eax
    mov eax, dword [rbp-32]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

section .data
    format db "%d", 10, 0