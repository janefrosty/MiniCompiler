section .text
    global main
    extern malloc
    extern printf
    extern free

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov rdi, 20
    call malloc
    mov [rbp-8], rax
    mov dword [rbp-16], 0
    mov rax, [rbp-8]
    mov rcx, [rbp-16]
    lea rax, [rax + rcx*4]
    mov [rbp-24], rax
    mov dword [rbp-32], 10
    mov rax, [rbp-24]
    mov ecx, dword [rbp-32]
    mov [rax], ecx
    mov dword [rbp-40], 1
    mov rax, [rbp-8]
    mov rcx, [rbp-40]
    lea rax, [rax + rcx*4]
    mov [rbp-48], rax
    mov dword [rbp-56], 20
    mov rax, [rbp-48]
    mov ecx, dword [rbp-56]
    mov [rax], ecx
    mov dword [rbp-64], 0
    mov rax, [rbp-8]
    mov rcx, [rbp-64]
    lea rax, [rax + rcx*4]
    mov [rbp-72], rax
    mov rax, [rbp-72]
    mov ecx, [rax]
    mov dword [rbp-80], ecx
    mov dword [rbp-88], 1
    mov rax, [rbp-8]
    mov rcx, [rbp-88]
    lea rax, [rax + rcx*4]
    mov [rbp-96], rax
    mov rax, [rbp-96]
    mov ecx, [rax]
    mov dword [rbp-104], ecx
    mov eax, dword [rbp-80]
    add eax, dword [rbp-104]
    mov dword [rbp-112], eax
    mov eax, dword [rbp-112]
    mov dword [rbp-120], eax
    mov eax, dword [rbp-120]
    mov dword [rbp-128], eax
    mov eax, dword [rbp-128]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

section .data
    format db "%d", 10, 0