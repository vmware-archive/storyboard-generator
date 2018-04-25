import json
import os
import os.path
from storyboardgenerator.comicstrip import ComicStrip, Panel, RenderedActor, Words

#actorAttributeTypesDirectories = ['Arms', 'Bodies', 'Accessories', 'Faces', 'Heads']

# map of string characteristics -> list of assets

ASSET_DIRECTORY = os.path.join(os.path.dirname(__file__), "../../assets/")

ASSET_DIRECTORY = "/assets"

def metadata_types(directory=ASSET_DIRECTORY):
    for root, dirs, files in os.walk(directory):
        print("metadata_types inspecting directory {}/".format(root))
        if 'metadata.json' in files:
            print("Found metadata.json inside {}/".format(root))
            yield os.path.basename(root)

actorAttributeTypesDirectories = list(metadata_types())

print("Loaded actorAttributeTypesDirectories: {}".format(actorAttributeTypesDirectories))


def load_metadata(directory=ASSET_DIRECTORY, serve_at="/assets/"):
    actorAttributes = {}

    for root, dirs, files in os.walk(directory):
        print("load_metadata inspecting directory {}/".format(root))
        if 'metadata.json' in files:
            print("Found metadata.json inside {}/".format(root))
            typeDirectory = os.path.basename(root)
            with open(os.path.join(root, 'metadata.json')) as json_data:
                d = json.load(json_data)
                print("Loaded JSON:")
                print(d)

                # get the list of assets
                assets = d['files']

                for asset in assets:
                    # loop over the characteristics of the asset
                    for characteristic in asset['characteristics']:
                        # make sure the characteristic exists in the attribute map
                        if characteristic not in actorAttributes:
                            actorAttributes[characteristic] = []

                        # get the asset information
                        url = '/assets/{0}/{1}'.format(typeDirectory, asset['url'])
                        assetType = asset['type']

                        # add the asset to the characteristic map
                        actorAttributes[characteristic].append(
                            dict([('url', url), ('type', assetType)])
                        )

    print('--- Imported Attributes ---')
    return actorAttributes


actorAttributes = load_metadata()


def getCharacteristic(characteristic, type=None, invert=False):
    if characteristic not in actorAttributes:
        return None

    assets = actorAttributes[characteristic]

    if type is not None:
        if invert:
            assets = [asset for asset in assets if asset['type'] != type]
        else:
            assets = [asset for asset in assets if asset['type'] == type]

    return assets


def renderComicStrip(comic):
    print('--- Render ---')
    print(comic)

    # define a response dictionary that will hold our final results
    response = {}

    # TODO: loop over comic and piece together the
    response['title'] = comic.name
    response['panels'] = []

    for panel in comic.children(Panel):
        response['panels'].append(renderPanel(panel))

    # generate the json from the response
    json_data = json.dumps(response)
    print('--- Final Response ---')
    print(json_data)
    return json_data


def renderPanel(panel):
    response = {
        "caption": panel.name,
        "layer": {}
    }

    # Background / Location
    for prop in panel.props:
        print('prop:', prop)
        assets = getCharacteristic(prop, 'location')
        print('assets:', assets)
        if assets is not None and assets.__len__() > 0:
            response['layer']['url'] = assets[0]['url']
            response['layer']['type'] = assets[0]['type']

    # Narration
    if panel.narration is not None:
        response['caption'] = panel.narration._data

    # Actors
    actors = []
    for i, actor in enumerate(panel.children(RenderedActor)):
        actors.extend(renderActor(actor, i))
    response['layer']['children'] = actors

    return response


def renderActor(actor, i=0):
    print('actor', i, actor)

    # Build a stock actor
    actorBody = {
        'body': getCharacteristic('default', 'body')[0],
        'head': getCharacteristic('default', 'head')[0],
        'face': getCharacteristic('default', 'face')[0],
        'arms': getCharacteristic('default', 'arms')[0],
        'accessories': []
    }

    def actorContainsAccessoryType(type):
        for asset in actorBody['accessories']:
            if asset['type'] == type:
                return True
        return False

    # Mutate the stock actor based on 'props'
    for prop in actor.props:
        print('prop:', prop)
        assets = getCharacteristic(prop, 'location', True)
        print('assets:', assets)
        if assets is not None:
            # TODO: Better strategy for picking which asset to use for each type
            for asset in assets:
                t = asset['type']
                if t == 'body':
                    actorBody['body'] = asset
                elif t == 'head':
                    actorBody['head'] = asset
                elif t == 'face':
                    actorBody['face'] = asset
                elif t == 'arms':
                    actorBody['arms'] = asset
                else:
                    if not actorContainsAccessoryType(asset['type']):
                        actorBody['accessories'].append(asset)

    print('final actor:', actorBody)

    # Convert the actor into asset model
    response = {
        'url': actorBody['body']['url']
    }

    # add the modeled body properties
    children = []
    children.extend([
        { 'url': actorBody['head']['url'] },
        { 'url': actorBody['face']['url'] },
        { 'url': actorBody['arms']['url'] }
    ])

    # add the accessories
    for accessory in actorBody['accessories']:
        children.append({ 'url': accessory['url']})

    response['children'] = children

    # TODO: position information?
    response['position'] = i



    # add the speech
    # We treat the speech as another actor
    speech = {}
    words = actor.children(Words)
    if words is not None:
        for text in words:
            speech['text'] = text._data
            speech['type'] = text._kind
            speech['position'] = i + 1



    return [response, speech]


def main():
    load_metadata()

    comic = ComicStrip()
    comic.name = 'My First Story'

    panel = Panel()
    panel.name = 'Is this thing on?'
    comic.append(panel)

    bob = RenderedActor()
    bob.name = 'Bob'
    bob.props.extend(['happy', 'serious'])
    panel.append(bob)

    bobTalk = Words()
    bobTalk._data = "hello world!"
    bob.append(bobTalk)

    alice = RenderedActor()
    alice.name = 'Alice'
    alice.props.extend(['sad', 'bow'])
    panel.append(alice)


    renderComicStrip(comic)


if __name__ == "__main__":
    main()
