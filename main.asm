section .text
    global main

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], 42    ; x = 42
    mov dword [rbp-16], eax         ; t1
    mov eax, t1
    jmp .return_label
    mov rsp, rbp
    pop rbp
    ret
