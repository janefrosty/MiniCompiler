section .text
    global main
    extern printf

main:
    push rbp
    mov rbp, rsp
    sub rsp, 128
    mov dword [rbp-8], 10
    mov dword [rbp-8], eax
    mov dword [rbp-8], 5
    mov eax, t2
    add eax, t3
    mov [rbp-16], eax
    mov eax, 0
    jmp .return_label
    mov eax, 0
    jmp .return_label
    mov rsp, rbp
    pop rbp
    ret

section .data
    format db "%d", 10, 0