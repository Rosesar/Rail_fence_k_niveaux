import streamlit as st
import matplotlib.pyplot as plt


def encrypt_rail_fence(text, k):
    """Encrypt the given text using Rail Fence Cipher with k rails."""
    rail = [['' for _ in range(len(text))] for _ in range(k)]
    direction_down = False
    row, col = 0, 0

    for char in text:
        rail[row][col] = char
        if row == 0 or row == k - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
        col += 1

    result = []
    for r in rail:
        for c in r:
            if c != '':
                result.append(c)

    visualize_rail(rail, "Modèle de chiffrement en Rail Fence")
    return ''.join(result)


def decrypt_rail_fence(cipher, k):
    """Decrypt ciphertext using Rail Fence Cipher with k rails."""
    rail = [['' for _ in range(len(cipher))] for _ in range(k)]
    direction_down = None
    row, col = 0, 0

    for i in range(len(cipher)):
        rail[row][col] = '*'
        if row == 0 or row == k - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
        col += 1

    index = 0
    for r in range(k):
        for c in range(len(cipher)):
            if rail[r][c] == '*':
                rail[r][c] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    direction_down = None
    for i in range(len(cipher)):
        result.append(rail[row][col])
        if row == 0 or row == k - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
        col += 1

    visualize_rail(rail, "Modèle de déchiffrement en Rail Fence")
    return ''.join(result)


def visualize_rail(matrix, title):
    """Visualizes a rail matrix for encryption or decryption."""
    fig, ax = plt.subplots(figsize=(10, len(matrix)))
    ax.set_title(title)
    ax.axis('off')

    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            if char != '':
                ax.text(j, -i, char, fontsize=12, ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='lightblue'))
    
    ax.set_xlim(-1, len(matrix[0]))
    ax.set_ylim(-len(matrix), 1)
    plt.gca().invert_yaxis()
    st.pyplot(fig)


# Streamlit Interface
st.title("Rail Fence avec k niveaux ")

# Input for plaintext or ciphertext
operation = st.radio("Choisir l\'opération ", ["Chiffrement", "Déchiffrement"])
k = st.number_input("Entrer le nombre de niveaux  (k):", min_value=2, max_value=100, value=3, step=1)

# File upload section
uploaded_file = st.file_uploader("Télécharger un fichier .txt", type="txt")

if uploaded_file:
    # Read file content
    text = uploaded_file.read().decode("utf-8")
    st.write("Le contenu du fichier téléchargé :")
    st.text(text)
else:
    # Fallback to manual input
    text = st.text_input("Entrer tle texte:", " ")

if st.button("Appliquer l\'opération"):
    if operation == "Chiffrement":
        st.subheader("Résultat du chiffrement")
        encrypted_text = encrypt_rail_fence(text, k)
        st.write(f"Le texte chiffré: **{encrypted_text}**")
        # Provide a download button
        st.download_button("Télécharger le texte chiffré ", data=encrypted_text, file_name="texte_chiffre.txt", mime="text/plain")
    elif operation == "Déchiffrement":
        st.subheader("Résultat du déchiffrement")
        decrypted_text = decrypt_rail_fence(text, k)
        st.write(f"Decrypted Text: **{decrypted_text}**")
        # Provide a download button
        st.download_button("Télécharger le texte déchiffré", data=decrypted_text, file_name="texte_dechiffre.txt", mime="text/plain")
