def display_json(json_data):
    import streamlit as st
    import json
    import base64
    from PIL import Image
    from io import BytesIO

    # Parse JSON if it's a string
    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
            st.text(json_data)
            return
    else:
        data = json_data

    # Check for errors in the response
    if "error" in data:
        st.error(f"Processing Error: {data['error']}")
        return

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📝 Text Content", "🖼️ Images", "📋 Raw JSON"])
    
    with tab1:
        st.subheader("PDF Processing Summary")
        if "metadata" in data:
            metadata = data["metadata"]
            
            # Display key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Pages", metadata.get("pageCount", "N/A"))
            with col2:
                text_length = len(data.get("text", ""))
                st.metric("Characters Extracted", f"{text_length:,}")
            with col3:
                image_count = len(data.get("images", []))
                st.metric("Images Found", image_count)
            
            # Display metadata in a nice format
            st.subheader("Document Information")
            col1, col2 = st.columns(2)
            
            with col1:
                if metadata.get("title"):
                    st.write(f"**Title:** {metadata['title']}")
                if metadata.get("author"):
                    st.write(f"**Author:** {metadata['author']}")
                if metadata.get("subject"):
                    st.write(f"**Subject:** {metadata['subject']}")
            
            with col2:
                if metadata.get("creator"):
                    st.write(f"**Creator:** {metadata['creator']}")
                if metadata.get("producer"):
                    st.write(f"**Producer:** {metadata['producer']}")
                if metadata.get("creationDate"):
                    st.write(f"**Created:** {metadata['creationDate']}")
    
    with tab2:
        st.subheader("Extracted Text Content")
        text_content = data.get("text", "")
        if text_content.strip():
            st.text_area("Text Content", text_content, height=400)
            
            # Add download button for text
            st.download_button(
                label="📥 Download Text",
                data=text_content,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        else:
            st.info("No text content found in the PDF.")
    
    with tab3:
        st.subheader("Extracted Images")
        images = data.get("images", [])
        if images:
            st.write(f"Found {len(images)} image(s) in the PDF:")
            
            # Display images in a grid
            cols = st.columns(3)
            for i, img_data in enumerate(images):
                with cols[i % 3]:
                    try:
                        # Remove the data URL prefix if present
                        if img_data.startswith("data:image"):
                            img_data = img_data.split(",")[1]
                        
                        # Decode base64 image
                        img_bytes = base64.b64decode(img_data)
                        img = Image.open(BytesIO(img_bytes))
                        
                        st.image(img, caption=f"Image {i+1}", use_column_width=True)
                        
                        # Add download button for each image
                        st.download_button(
                            label=f"📥 Download Image {i+1}",
                            data=img_bytes,
                            file_name=f"extracted_image_{i+1}.jpg",
                            mime="image/jpeg",
                            key=f"img_{i}"
                        )
                    except Exception as e:
                        st.error(f"Error displaying image {i+1}: {str(e)}")
        else:
            st.info("No images found in the PDF.")
    
    with tab4:
        st.subheader("Raw JSON Output")
        st.json(data)
        
        # Add download button for JSON
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name="pdf_extraction_result.json",
            mime="application/json"
        )