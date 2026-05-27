section .text
    global main
    extern printf

factorial:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], eax
    mov dword [rbp-8], 1
    mov eax, t2
    add eax, t3
    mov [rbp-16], eax
    mov eax, 0
    jmp .return_label
    mov dword [rbp-8], eax
    mov eax, t5
    add eax, t6
    mov [rbp-16], eax
    mov eax, 0
    jmp .return_label
    mov rsp, rbp
    pop rbp
    ret

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], eax
    mov dword [rbp-8], eax
    mov eax, 0
    jmp .return_label
    mov rsp, rbp
    pop rbp
    ret

section .data
    format db "%d", 10, 0