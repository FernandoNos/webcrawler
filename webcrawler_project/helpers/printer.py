def print_tree(node,space,result):
    result = result +  u''.join((space,node.data,'[',node.type,']\n')).encode('utf-8')
    space = space + '|'
    node.checked = True
    for child in node.children:
        if not child.checked:
            result = result + print_tree(child,space,'')
        else:
            result = result + u''.join((space,child.data,'[',child.type,']**\n')).encode('utf-8')

    return result

def save_tree(node):
	file = open('sitemap.txt','w')
	result = print_tree(node,'','')
	print result
	file.write(result)
	file.close()