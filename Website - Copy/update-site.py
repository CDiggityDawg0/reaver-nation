import os
import shutil
import sys
import fileinput


text_file = "Products.txt"
source_file = "product-details-template.html"
productsMade = False


def alterFile(product_variables):
    productName = product_variables[0]
    price = product_variables[1]
    category = product_variables[2]
    desc = product_variables[3]
    image1 = product_variables[4].replace("\"", "")
    image2 = product_variables[5].replace("\"", "")
    image3 = product_variables[6].replace("\"", "")
    image4 = product_variables[7].replace("\"", "")
    destination_file = "product-details-" + productName.replace(" ", "-").lower() + ".html"

    os.makedirs(f"images\\{productName}", exist_ok=True)
    filename, file_extension = os.path.splitext(image1)
    shutil.copy(image1, f"images\\{productName}\\image1{file_extension}")
    image1 = f"images\\{productName}\\image1{file_extension}"
    shutil.copy(image2, f"images\\{productName}\\image2{file_extension}")
    image2 = f"images\\{productName}\\image2{file_extension}"
    shutil.copy(image3, f"images\\{productName}\\image3{file_extension}")
    image3 = f"images\\{productName}\\image3{file_extension}"
    shutil.copy(image4, f"images\\{productName}\\image4{file_extension}")
    image4 = f"images\\{productName}\\image4{file_extension}"

    print(f"Created {destination_file}! \n Replacing placeholders...")
    f = open(source_file,'r')
    filedata = f.read()
    f.close()
    
    newdata = filedata.replace("product_name",productName)
    newdata = newdata.replace("category",category)
    newdata = newdata.replace("price",price)
    newdata = newdata.replace("description",desc)
    newdata = newdata.replace("img_1_replace",image1)
    newdata = newdata.replace("img_2_replace",image2)
    newdata = newdata.replace("img_3_replace",image3)
    newdata = newdata.replace("img_4_replace",image4)

    f = open(destination_file,'w')
    f.write(newdata)
    f.close()

    global productsMade
    #If the products page has been made, just use the current product page
    #otherwise use template
    if(not productsMade):
        print(f"Modifying product page...")
        f = open('products-template.html','r')
        filedata = f.read()
        f.close()

        f = open('products.html','w')
        f.write(filedata)
        f.close()
    else:
        print(f"Modifying product page...")
        f = open('products.html','r')
        filedata = f.read()
        f.close()
    

    

    file = open('products.html')
    # read the file as a list
    data = file.readlines()
    # close the file
    file.close()
    newdata = filedata

    added = False
    current_line = 0
    while(current_line < len(data) and not added):
        if("<!--Start row-->" in data[current_line]):
            current_line += 1
            if("<div class=\"row\">" in data[current_line]):
                i = 0
                while(i < 4):
                    print(i)
                    if("<div class=\"col-4\">" in data[current_line + 1]):
                        current_line += 4
                    else:
                        data.insert(current_line + 1, f"<div class=\"col-4\">\n<a href=\"{destination_file}\"><img src=\"{image1}\"></a>\n<a href=\"{destination_file}\"><h4 style=\"color: #3e5974;\">{productName}</h4></a>\n<p style=\"color: #3e5974; font-size: 20px;\">${price}</p></div>\n")
                        added = True
                        break
                    i += 1
            else:
                data.insert(current_line, f"<div class=\"row\">\n<div class=\"col-4\">\n<a href=\"{destination_file}\"><img src=\"{image1}\"></a>\n<a href=\"{destination_file}\"><h4 style=\"color: #3e5974;\">{productName}</h4></a>\n<p style=\"color: #3e5974; font-size: 20px;\">${price}</p></div>\n</div>\n<!--Start row-->")
                added = True

        current_line += 1


    newdata = ''
    current_line = 0
    while(current_line < len(data)):
        newdata += data[current_line]
        current_line += 1

    f = open('products.html','w')
    f.write(newdata)
    f.close()
    productsMade = True
    

    

def analyze():
    print(f"Analyzing {text_file}")
    #Go line by line to analyze txt file
    current_line = 0
    while(current_line < len(data)):
        #A new product page must be created
        if("[New Product]" in data[current_line] and data[current_line][0] != "#"):
            print("Product Found!")
            #establish variables
            product_variables = []

            # productName = 0
            # price = 1
            # category = 2 
            # desc = 3
            # image1 = 4
            # image2 = 5
            # image3 = 6
            # image4 = 7

            startingline = current_line
            current_line += 1
            while(current_line <= startingline + 8):
                
                #Skip line if it is a comment
                if(data[current_line][0] == "#"):
                    current_line += 1
                    startingline += 1
                else:
                    product_variables.append(data[current_line].split("\n")[0].split("#")[0])
                    current_line += 1
            alterFile(product_variables)
        current_line += 1


try:
    # open the data file
    file = open(text_file)
    # read the file as a list
    data = file.readlines()
    # close the file
    file.close()
    
    analyze()
except FileNotFoundError:
    print(f"File \'{text_file}\' could not be found. Ensure your product txt file has this name")


input("Press enter to close")