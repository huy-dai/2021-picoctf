	.arch armv8-a
	.file	"chall_2.c"
	.text
	.align	2
	.global	func1
	.type	func1, %function
func1:
	sub	sp, sp, #32
	str	w0, [sp, 12] # Store w0 at sp+12 = 3736234946
	str	wzr, [sp, 24] # Zeroes out sp+24 = var1
	str	wzr, [sp, 28] # Zeroes out sp+28 = var2
	b	.L2
.L3:
	ldr	w0, [sp, 24] 
	add	w0, w0, 3 
	str	w0, [sp, 24] # Add var1 by 3
 	ldr	w0, [sp, 28] 
	add	w0, w0, 1 
	str	w0, [sp, 28] # Add var2 by 1
.L2:
	ldr	w1, [sp, 28] # w1 = var2
	ldr	w0, [sp, 12] # w0 = input = 3736234946
	cmp	w1, w0 # Set carry flag if no borrow
	bcc	.L3 # Branch if carry flag not set (e.g., w1 >= w0)
	ldr	w0, [sp, 24] # Return var1
	add	sp, sp, 32
	ret
	.size	func1, .-func1
	.section	.rodata
	.align	3
.LC0:
	.string	"Result: %ld\n"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
	stp	x29, x30, [sp, -48]! # Store x29 and x30 at sp-48
	add	x29, sp, 0 # x29 = sp
	str	w0, [x29, 28] # Stores w0 or "3736234946" into sp+28

	# The following converts the w0 string into an integer
	str	x1, [x29, 16] # Stores x1 at sp+16
	ldr	x0, [x29, 16] # Loads x1 into x0
	add	x0, x0, 8 
	ldr	x0, [x0] 
	bl	atoi
	# w0 = 3736234946 (integer)

	bl	func1
	str	w0, [x29, 44] 
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	ldr	w1, [x29, 44]
	bl	printf
	nop
	ldp	x29, x30, [sp], 48
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
