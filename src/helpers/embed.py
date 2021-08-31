import discord.ext
import discord

  
def full_embed(
    title:str=None, 
    description:str=None, 
    url:str=None, 
    colour=discord.Color.blue(), 

    fields:dict=None,
    fields_inline=True, 
    thumbnail:str=None, 
    footer:str=None, 

    author_name:str=None, 
    author_url:str=None, 
    author_icon:str=None,
    blank=False
    ):

    
    if blank == False:
        if description is None:
            if url is None:
                embed=discord.Embed(title=title[:256], color=colour)
            else:
                embed=discord.Embed(title=title[:256], url=url, color=colour)
            
        else:
            if url is None:
                embed=discord.Embed(title=title[:256], description=description, color=colour)
            else:
                embed=discord.Embed(title=title[:256], url=url, description=description, color=colour)
    else:
        embed=discord.Embed()


    if fields is not None:
        for key, value in fields.items():
            embed.add_field(name=key[:256], value=value[:1024], inline=fields_inline)

    if author_name is not None:
        if author_url is not None:
            embed.set_author(name=author_name[:256], url=author_url, icon_url=author_icon)
        else:
            embed.set_author(name=author_name[:256], icon_url=author_icon)

    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)

    if footer is not None:
        embed.set_footer(text=footer[:2048])

    return embed
