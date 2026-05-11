section .text
    global main

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], 10    ; x = 10
    mov dword [rbp-16], eax         ; t2
    mov dword [rbp-24], 5    ; t3 = 5
    mov eax, t2
    mov [rbp-32], eax
    cmp t1, 0
    je L1
    mov eax, 1
    jmp .return_label
    jmp L2
L1:
    mov eax, 0
    jmp .return_label
L2:
    mov rsp, rbp
    pop rbp
    ret
