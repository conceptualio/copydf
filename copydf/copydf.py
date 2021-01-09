from IPython import get_ipython
import re

def copyDF( df ):
    '''
    A function that copies a dataframe to your clipboard when run in Jupyter.
    
    Args:
        * df (``pandas.DataFrame``): a dataframe to copy to the local clipboard
    
    Returns:
        None
    '''
    ipy = get_ipython()
    ipy.run_cell_magic( "javascript", "",
        '''
        function copyToClipboard(text) {
            if ( window.clipboardData && window.clipboardData.setData ) { return clipboardData.setData( "Text", text ); }
            else if ( document.queryCommandSupported && document.queryCommandSupported( "copy" ) ) {
                var textarea = document.createElement( "textarea" );
                textarea.textContent = text;
                textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
                document.body.appendChild( textarea );
                textarea.select();
                try { return document.execCommand( "copy" ); }
                catch ( ex ) {
                    console.warn( "Copy to clipboard failed.", ex );
                    return false;
                }
                finally { document.body.removeChild( textarea ); }
            }
        };
        copyToClipboard( "%s" );
        ''' % ( "{}{}".format( 
                "\t{}\\n".format( "\t".join( [ str( df.columns[ c ] ) for c in range( len( df.columns ) ) ] ) ),
                "\\n".join( [ "{}\t{}".format( str( df.index[ r ] ), "\t".join( [ str( df.iloc[ r, c ] ) for c in range( len( df.columns ) ) ] ) ) for r in range( len( df ) ) ] )
            ) ) )
