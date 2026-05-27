section .text
    global main

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], 0    ; i = 0
L1:
    mov dword [rbp-16], eax         ; t2
    mov dword [rbp-24], 10    ; t3 = 10
    mov eax, t2
    mov [rbp-32], eax
    cmp t1, 0
    je L2
    mov dword [rbp-40], eax         ; t5
    mov dword [rbp-48], 1    ; t6 = 1
    mov eax, t5
    add eax, t6
    mov [rbp-56], eax
    mov dword [rbp-8], eax         ; i
    jmp L1
L2:
    mov dword [rbp-64], eax         ; t7
    mov eax, t7
    jmp .return_label
    mov rsp, rbp
    pop rbp
    ret
