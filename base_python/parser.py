from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 translate: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
	 yrotate: create an y-axis rotation matrix,w
	    then multiply the transform matrix by the rotation matrix -
	    takes 1 argument (theta)
	 zrotate: create an z-axis rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 1 argument (theta)
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""
def parse_file( fname, points, transform, screen, color ):
    one_liners = {'ident': ident, 'apply': matrix_mult, 'display': display}
    two_liners = {'line': add_edge, 'scale': make_scale, 'move': make_translate, 'rotate': 'make_rot', 'save': save_extension}
    with open(fname) as file_:
        file_content = file_.readlines()
    for index, line in enumerate(file_content):
        line = line.strip()
        if line[0].isdigit() or file_content[index - 1].strip() == 'rotate' or file_content[index - 1].strip() == 'save':
            continue
        if line in one_liners:
            if line == 'ident':
                one_liners[line](transform)
            elif line == 'apply':
                one_liners[line](transform, points)
            else:
                clear_screen(screen)
                draw_lines(points, screen, color)
                one_liners[line](screen)
        elif line in two_liners:
            if line == 'line':
                next_line = file_content[index + 1].strip()
                args = next_line.split(' ')  
                if len(args) < 6 or len(args) > 6:
                    # Add one more to index + 1 because of zero-based index
                    print 'Line ' + str(index + 2) + ' has ' + str(len(args)) + ' arguments, expecting 6...'
                else:
                    try:
                        two_liners[line](points, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                    except ValueError:
                        # Add one more to index + 1 because of zero-based index
                        print 'Line ' + str(index + 2) + ' contains non-numerical values...'
            elif line == 'scale':
                next_line = file_content[index + 1].strip()
                args = next_line.split(' ')  
                if len(args) < 3 or len(args) > 3:
                    # Add one more to index + 1 because of zero-based index
                    print 'Line ' + str(index + 2) + ' has ' + str(len(args)) + ' arguments, expecting 3...'
                else:
                    try:
                        scale_matrix = two_liners[line](float(args[0]), float(args[1]), float(args[2]))
                        matrix_mult(scale_matrix, transform)
                    except ValueError:
                        # Add one more to index + 1 because of zero-based index
                        print 'Line ' + str(index + 2) + ' contains non-numerical values...'
            elif line == 'move':
                next_line = file_content[index + 1].strip()
                args = next_line.split(' ')  
                if len(args) < 3 or len(args) > 3:
                    # Add one more to index + 1 because of zero-based index
                    print 'Line ' + str(index + 2) + ' has ' + str(len(args)) + ' arguments, expecting 3...'
                else:
                    try:
                        translate_matrix = two_liners[line](float(args[0]), float(args[1]), float(args[2]))
                        matrix_mult(translate_matrix, transform)
                    except ValueError:
                        # Add one more to index + 1 because of zero-based index
                        print 'Line ' + str(index + 2) + ' contains non-numerical values...'
            elif line == 'rotate':
                next_line = file_content[index + 1].strip()
                args = next_line.split(' ')  
                if len(args) < 2 or len(args) > 2:
                    # Add one more to index + 1 because of zero-based index
                    print 'Line ' + str(index + 2) + ' has ' + str(len(args)) + ' arguments, expecting 2...'
                else:
                    if args[0] in 'xyzXYZ':
                        function = eval(two_liners[line] + args[0].upper())
                    else:
                        print 'Line ' + str(index + 2) + ' provided an invalid axis...'
                        raise SystemExit(1)                    
                    try:
                        rotate_matrix = function(float(args[1]))
                        matrix_mult(rotate_matrix, transform)
                    except ValueError:
                        # Add one more to index + 1 because of zero-based index
                        print 'Line ' + str(index + 2) + ' contains non-numerical values...'
            else:
                next_line = file_content[index + 1].strip()
                args = next_line.split(' ')                
                if len(args) < 1 or len(args) > 1:
                    # Add one more to index + 1 because of zero-based index
                    print 'Line ' + str(index + 2) + ' has ' + str(len(args)) + ' arguments, expecting 1...'
                else:
                    clear_screen(screen)
                    draw_lines(points, screen, color)
                    display(screen)
                    two_liners[line](screen, args[0])
        else:
            print 'Invalid command found at line ' + str(index)
            raise SystemExit(1)
