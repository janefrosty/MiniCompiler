section .text
    global main
    extern malloc
    extern printf
    extern free

fib:
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
    mov eax, dword [rbp-16]
    mov dword [rbp-40], eax
    mov eax, dword [rbp-40]
    jmp .return_label
    jmp L2
L1:
L2:
    mov eax, dword [rbp-16]
    mov dword [rbp-48], eax
    mov dword [rbp-56], 1
    mov eax, dword [rbp-48]
    sub eax, dword [rbp-56]
    mov dword [rbp-64], eax
    mov dword [rbp-72], 0
    mov eax, dword [rbp-16]
    mov dword [rbp-80], eax
    mov dword [rbp-88], 2
    mov eax, dword [rbp-80]
    sub eax, dword [rbp-88]
    mov dword [rbp-96], eax
    mov dword [rbp-104], 0
    mov eax, dword [rbp-72]
    add eax, dword [rbp-104]
    mov dword [rbp-112], eax
    mov eax, dword [rbp-112]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

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
    je L3
    mov eax, dword [rbp-40]
    jmp .return_label
    jmp L4
L3:
L4:
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
    mov rdi, 40
    call malloc
    mov [rbp-8], rax
    mov dword [rbp-16], 0
L5:
    mov eax, dword [rbp-16]
    mov dword [rbp-24], eax
    mov dword [rbp-32], 10
    mov eax, dword [rbp-24]
    mov dword [rbp-40], eax
    cmp dword [rbp-40], 0
    je L6
    mov eax, dword [rbp-16]
    mov dword [rbp-48], eax
    mov rax, [rbp-8]
    mov rcx, [rbp-48]
    lea rax, [rax + rcx*4]
    mov [rbp-56], rax
    mov eax, dword [rbp-16]
    mov dword [rbp-64], eax
    mov dword [rbp-72], 0
    mov rax, [rbp-56]
    mov ecx, dword [rbp-72]
    mov [rax], ecx
    mov eax, dword [rbp-16]
    mov dword [rbp-80], eax
    mov dword [rbp-88], 1
    mov eax, dword [rbp-80]
    add eax, dword [rbp-88]
    mov dword [rbp-96], eax
    mov eax, dword [rbp-96]
    mov dword [rbp-16], eax
    jmp L5
L6:
    mov dword [rbp-104], 0
    mov dword [rbp-112], 0
    mov eax, dword [rbp-112]
    mov dword [rbp-16], eax
L7:
    mov eax, dword [rbp-16]
    mov dword [rbp-120], eax
    mov dword [rbp-128], 10
    mov eax, dword [rbp-120]
    mov dword [rbp-136], eax
    cmp dword [rbp-136], 0
    je L8
    mov eax, dword [rbp-104]
    mov dword [rbp-144], eax
    mov eax, dword [rbp-16]
    mov dword [rbp-152], eax
    mov rax, [rbp-8]
    mov rcx, [rbp-152]
    lea rax, [rax + rcx*4]
    mov [rbp-160], rax
    mov rax, [rbp-160]
    mov ecx, [rax]
    mov dword [rbp-168], ecx
    mov eax, dword [rbp-144]
    add eax, dword [rbp-168]
    mov dword [rbp-176], eax
    mov eax, dword [rbp-176]
    mov dword [rbp-104], eax
    mov eax, dword [rbp-16]
    mov dword [rbp-184], eax
    mov dword [rbp-192], 1
    mov eax, dword [rbp-184]
    add eax, dword [rbp-192]
    mov dword [rbp-200], eax
    mov eax, dword [rbp-200]
    mov dword [rbp-16], eax
    jmp L7
L8:
    mov dword [rbp-208], 5
    mov dword [rbp-216], 0
    mov eax, dword [rbp-216]
    mov dword [rbp-224], eax
    mov eax, dword [rbp-104]
    mov dword [rbp-232], eax
    mov eax, dword [rbp-224]
    mov dword [rbp-240], eax
    mov eax, dword [rbp-232]
    add eax, dword [rbp-240]
    mov dword [rbp-248], eax
    mov eax, dword [rbp-248]
    mov dword [rbp-104], eax
    mov eax, dword [rbp-104]
    mov dword [rbp-256], eax
    mov eax, dword [rbp-256]
    jmp .return_label
.return_label:
    mov rsp, rbp
    pop rbp
    ret

section .data
    format db "%d", 10, 0