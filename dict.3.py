nest = "blorp"
dict = {
		"foo":'bar',
		"blah":'blorp',
		nest: {
			"nested":"child",
			"foo":"duplicate"
		}
	}


print(dict["blorp"]["nested"])