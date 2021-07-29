wp_url = 'http://fancy-wordpress-site.com'

xmlrpc_wrong_credentials_response = """
<methodResponse>
  <fault>
    <value>
      <struct>
        <member>
          <name>faultCode</name>
          <value><int>403</int></value>
        </member>
        <member>
          <name>faultString</name>
          <value><string>Incorrect username or password.</string></value>
        </member>
      </struct>
    </value>
  </fault>
</methodResponse>
"""

xmlrpc_right_admin_credentials_response = """
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><struct>
  <member><name>isAdmin</name><value><boolean>1</boolean></value></member>
  <member><name>url</name><value><string>http://fancy-wordpress-site.com/</string></value></member>
  <member><name>blogid</name><value><string>1</string></value></member>
  <member><name>blogName</name><value><string>Omega</string></value></member>
  <member><name>xmlrpc</name><value><string>http://fancy-wordpress-site.com/xmlrpc.php</string></value></member>
</struct></value>
</data></array>
      </value>
    </param>
  </params>
</methodResponse>
"""

xmlrpc_right_not_admin_credentials_response = """
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><struct>
  <member><name>isAdmin</name><value><boolean>0</boolean></value></member>
  <member><name>url</name><value><string>http://fancy-wordpress-site.com/</string></value></member>
  <member><name>blogid</name><value><string>1</string></value></member>
  <member><name>blogName</name><value><string>Omega</string></value></member>
  <member><name>xmlrpc</name><value><string>http://fancy-wordpress-site.com/xmlrpc.php</string></value></member>
</struct></value>
</data></array>
      </value>
    </param>
  </params>
</methodResponse>
"""

wordpress_themes_response = '<div class="theme active"><h2 class="theme-name" id="twentytwentyone-id">Fancy theme</h2></div>'

wordpress_theme_editor_response = """<form action="theme-editor.php" id="template" method="post" name="template">
<input id="nonce" name="nonce" type="hidden" value="12837987"/><input name="_wp_http_referer" type="hidden" value="/wp-admin/theme-editor.php?file=404.php&amp;theme=twentytwentyone"/> <div>
<label for="newcontent" id="theme-plugin-editor-label">Selected file content:</label>
<textarea aria-describedby="editor-keyboard-trap-help-1 editor-keyboard-trap-help-2 editor-keyboard-trap-help-3 editor-keyboard-trap-help-4" cols="70" id="newcontent" name="newcontent" rows="30">
&lt;?php
/**
 * The template for displaying 404 pages (not found)
 *
 * @link https://codex.wordpress.org/Creating_an_Error_404_Page
 *
 * @package WordPress
 * @subpackage Twenty_Twenty_One
 * @since Twenty Twenty-One 1.0
 */

get_header();
?&gt;

        &lt;header class="page-header alignwide"&gt;
                &lt;h1 class="page-title"&gt;&lt;?php esc_html_e( 'Nothing here', 'twentytwentyone' ); ?&gt;&lt;/h1&gt;
        &lt;/header&gt;&lt;!-- .page-header --&gt;

        &lt;div class="error-404 not-found default-max-width"&gt;
                &lt;div class="page-content"&gt;
                        &lt;p&gt;&lt;?php esc_html_e( 'It looks like nothing was found at this location. Maybe try a search?', 'twentytwentyone' ); ?&gt;&lt;/p&gt;
                        &lt;?php get_search_form(); ?&gt;
                &lt;/div&gt;&lt;!-- .page-content --&gt;
        &lt;/div&gt;&lt;!-- .error-404 --&gt;

&lt;?php
get_footer();
</textarea>
<input name="action" type="hidden" value="update"/>
<input name="file" type="hidden" value="404.php"/>
<input name="theme" type="hidden" value="twentytwentyone"/>
</div>
<div class="hide-if-no-js" id="documentation">
<label for="docs-list">Documentation:</label>
<select id="docs-list" name="docs-list"><option value="">Function Name…</option><option value="esc_html_e">esc_html_e()</option><option value="get_footer">get_footer()</option><option value="get_header">get_header()</option><option value="get_search_form">get_search_form()</option><option value="system">system()</option></select> <input class="button" disabled="" id="docs-lookup" onclick="if ( '' != jQuery('#docs-list').val() ) { window.open( 'https://api.wordpress.org/core/handbook/1.0/?function=' + escape( jQuery( '#docs-list' ).val() ) + '&amp;locale=en_US&amp;version=5.7.2&amp;redirect=true'); }" type="button" value="Look Up"/>
</div>
<div>
<div class="editor-notices">
</div>
<p class="submit">
<input class="button button-primary" id="submit" name="submit" type="submit" value="Update File"/> <span class="spinner"></span>
</p>
</div>
<script id="tmpl-wp-file-editor-notice" type="text/html">
                <div class="notice inline notice-{{ data.type || 'info' }} {{ data.alt ? 'notice-alt' : '' }} {{ data.dismissible ? 'is-dismissible' : '' }} {{ data.classes || '' }}">
                        <# if ( 'php_error' === data.code ) { #>
                                <p>
                                        Your PHP code changes were rolled back due to an error on line {{ data.line }} of file {{ data.file }}. Please fix and try saving again.       </p>
                                <pre>{{ data.message }}</pre>
                        <# } else if ( 'file_not_writable' === data.code ) { #>
                                <p>
                                        You need to make this file writable before you can save your changes. See <a href="https://wordpress.org/support/article/changing-file-permissions/">Changing File Permissions</a> for more information.                                </p>
                        <# } else { #>
                                <p>{{ data.message || data.code }}</p>

                                <# if ( 'lint_errors' === data.code ) { #>
                                        <p>
                                                <# var elementId = 'el-' + String( Math.random() ); #>
                                                <input id="{{ elementId }}"  type="checkbox">
                                                <label for="{{ elementId }}">Update anyway, even though it might break your site?</label>
                                        </p>
                                <# } #>
                        <# } #>
                        <# if ( data.dismissible ) { #>
                                <button type="button" class="notice-dismiss"><span class="screen-reader-text">Dismiss</span></button>
                        <# } #>
                </div>
        </script>
</form>"""


wordpress_os_detection_linux_response = """<html>OMEGA_HOST_OS = Linux</html>"""
wordpress_os_detection_windows_response = """<html>OMEGA_HOST_OS = WINT</html>"""
