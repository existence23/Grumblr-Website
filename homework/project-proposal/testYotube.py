# Sample python code for playlistItems.list

def playlist_items_list_by_playlist_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlistItems().list(
    **kwargs
  ).execute()

  return print_response(response)

playlist_items_list_by_playlist_id(client,
    part='snippet,contentDetails',
    maxResults=25,
    playlistId='PLBCF2DAC6FFB574DE')