section .text
    global print_int
    global exit_program

; void print_int(long long value)
print_int:
    push rbp
    mov rbp, rsp
    ; Простая реализация вывода числа будет добавлена позже
    ; Пока заглушка
    mov rax, 1          ; syscall write
    mov rdi, 1          ; stdout
    mov rsi, msg
    mov rdx, 6
    syscall
    pop rbp
    ret

exit_program:
    mov rax, 60         ; syscall exit
    xor rdi, rdi
    syscall

section .data
    msg db '42', 10     ; временная заглушка
