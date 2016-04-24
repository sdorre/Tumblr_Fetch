import requests
import urllib
import os

client_key = "AWqX3ZjruKEQpoEWHekVVMqExgaPVwyrl3wvt6bjNtqeEPkrJi"


def fetchTumblrBasic( site, offset=-1, limit=-1, timestamp=0):

    mlist = []

    # TODO need to control site variable before request
    url = 'http://api.tumblr.com/v2/blog/'+site+'/posts/photo?api_key='+client_key

    if(offset!=-1):
        url = url +'&offset=%d' % (offset*20)
    if(limit!=-1):
        url = url +'limit=%d' % limit

    r = requests.get(url)

    #print r.status_code
    if(r.status_code != 200):
        return None

    try:
        json = r.json()
    except ValueError:
        print "Couldn't fetch a Json structure from %s" % site
        return mlist

    # define a list to store each url
    posts = json.get('response').get('posts')

    for item in posts:
        #we should control here when post was created
        # item.get('date')
        photos = item.get('photos')

        for picture in photos:
            p = picture.get('original_size')
            width = p.get('width')
            height = p.get('height')
            if width > height and width >= 1280 :
                print p.get('url')
                mlist.append(p.get('url'))

    return mlist



def fetchTumblr( site, nbOfPost ):
# each request made on Tumblr ebsite only give you 20 posts. 
# we handle this by requesting 20 post by 20
    q = nbOfPost // 20
    mod = nbOfPost % 20

    mlist = []

    for offset in range(0,q):
        result = fetchTumblrBasic(site, offset)
        if(result == None):
            print "failed to fetch tumblr %s : bad request"%site
            return

        mlist = mlist + result
        print 'fetch %d time'% (offset+1)

    mlist = mlist + fetchTumblrBasic(site, q, mod)
    print "fetched %d posts from tumblr %s" % (len(mlist), site)

    return mlist



def saveTumblrInFile( mlist, folderName):
#mlist contains all url we want to download
#folderName is the destination folder where to store all pictures
#each picture have a name like "tumblr_n7fot8vm1C1tytkpfo1_1280.jpg"
#the name seems to be unique for each image (at least for the same blog)

    cpt = 0
    for item in mlist:
        index = item.find('tumblr_')
        fileToSave = "%s/%s" % (folderName, item[index:])

        if not os.path.exists(fileToSave):
            print "Saving %s..."%fileToSave
            f = open(fileToSave, 'wb')
            f.write(urllib.urlopen(item).read())
            f.close()
        else:
            print "%s already exists!!"%fileToSave



if __name__ == '__main__':


#---------Read file 'TumblrList.txt' and extract all post from here-----------------

    homedir = "Tumblr"
    txt = open('TumblrList.txt')
    data = txt.read().splitlines()
    
    if not os.path.exists(homedir):
        os.makedirs(homedir)

    for line in data:
        folderName = homedir+"/"+line        
        fileToSaveName = folderName+"/"+line

        print "================================================"
        pictures = fetchTumblr(line, 100)
        print "================================================"

        if pictures:  
            if not os.path.exists(folderName):
                os.makedirs(folderName)

            # saving the list - all image that will be downloaded
            #txtToSave = open(fileToSaveName+".txt", 'w')

            #for item in set(pictures):
            #    txtToSave.write("%s\n"% item)

            #txtToSave.close()

            #download all big pictures
            saveTumblrInFile(set(pictures), folderName)
        else:
            print "Nothing to see on ", line

    txt.close();

#---------write your tumblr and the number of post you need to extract-----------------
    print "give the Tumblr you want to extract (without http or '/' characters"
    response = raw_input('Give URL here: ')
    while (response != ''):
        number = int(raw_input('How much post do you want ? '))

        list = fetchTumblr(response, number)

        response = raw_input('Give URL here: ')
